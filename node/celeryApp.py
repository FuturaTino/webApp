from celery import Celery
from celery import Task 
import time
from dotenv import load_dotenv,find_dotenv
import os
from pathlib import Path
import shutil 
from kombu import Queue
from core.colmap.convert import convert_video_to_images,convert_images_to_colmap
from core.dependencies import get_db
from core.oss import upload_file,prepare_job,delete_local_dir,get_oss_image_url,get_oss_ply_url
from core.reconstruct.train import training

from crud.captures import update_capture_status,STATUS,update_capture_info
import torch 
from celery.utils.log import get_task_logger

load_dotenv(find_dotenv("config.env"))
username = os.environ.get("REDIS_USER")
password = os.environ.get("REDIS_PASSWORD")
host = os.environ.get("REDIS_HOST")
port = os.environ.get("REDIS_PORT")
logger = get_task_logger(__name__)
app = Celery(__name__,  
             broker=f'redis://{username}:{password}@{host}:{port}/0',
             backend=f'redis://{username}:{password}@{host}:{port}/1')


# celery settings from https://docs.celeryq.dev/en/stable/userguide/configuration.html
app.conf.broker_connection_retry_on_startup = True
app.conf.worker_max_tasks_per_child = 1 # PoolWorker子进程在执行1个任务后重启，可以防止内存泄露。
app.conf.worker_concurrency = 2
app.conf.task_soft_time_limit=7200
app.conf.task_time_limit=7200
app.conf.task_default_exchange_type = 'fanout' # 广播模式


class ReconstructTask(Task):
    def before_start(self, task_id, args, kwargs):
        update_capture_status(db=next(get_db()),uuid=task_id,status=STATUS['PreProcessing'])
        try:
            prepare_job(uuid=task_id)
            logger.info(f"Task: {task_id},Status: {STATUS['PreProcessing']}")
        except Exception as e:
            update_capture_status(db=next(get_db()),uuid=task_id,status=STATUS['Failed'])
            logger.info(f"Task: {task_id},Status: {STATUS['Failed']}")
            raise e 

    def on_success(self, retval, task_id, args, kwargs):
        update_capture_status(db=next(get_db()),uuid=task_id,status=STATUS['Success'])
        logger.info(f"Task: {task_id},Status: {STATUS['Success']} ✅ ")
        work_dir = Path(os.getenv('STORAGE_DIR')) / task_id
        # delete_local_dir(work_dir)


    def on_failure(self, exc, task_id, args, kwargs, einfo):
        update_capture_status(db=next(get_db()),uuid=task_id,status=STATUS['Failed'])
        work_dir = Path(os.getenv('STORAGE_DIR')) / task_id
        # delete_local_dir(work_dir)
        logger.info(f"Task: {task_id},Status: {STATUS['Failed']}")

@app.task(bind=True,base=ReconstructTask) # bind=True 会将task(这里是customTask)实例作为第一个参数传入
def reconstruct(self,uuid):
    work_dir:Path = Path(os.getenv('STORAGE_DIR')) / uuid
    video_path:Path = work_dir / f"{uuid}.mp4"
    ply_path = work_dir / f"{uuid}.ply"
    image_dir = work_dir / "input"
    if not video_path.exists():
        update_capture_status(db=next(get_db()),uuid=uuid,status=STATUS['Failed'])
        raise FileNotFoundError(f"Video file not found: {video_path}")

    convert_video_to_images(video_path=video_path,image_dir=image_dir,num_frames_target=450)
    convert_images_to_colmap(source_path=work_dir,no_gpu=False,verbose=False)
    

    # train model ,uplaod the ply  and share the url
    update_capture_status(db=next(get_db()),uuid=uuid,status=STATUS['Reconstructing'])
    try:
        training(source_path=work_dir,model_path=work_dir, uuid=uuid,saving_iterations=[30000])
        upload_file(oss_key=f"ply/{uuid}.ply",local_path=str(ply_path))
        image_url = get_oss_image_url(object_name=uuid)
        result_url = get_oss_ply_url(object_name=uuid)
        update_capture_info(db=next(get_db()),uuid=uuid,image_url=image_url,result_url=result_url)
    except Exception as e:
        raise e

