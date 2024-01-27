from celery import Celery
from celery import Task 
import time
from dotenv import load_dotenv,find_dotenv
import os
from pathlib import Path
import shutil 
from convert import convert_video_to_images,convert_images_to_colmap

from crud.captures import update_capture_status,STATUS
from core.dependencies import get_db

root_dir = Path(__file__).parent.parent.parent # app dir 
load_dotenv(find_dotenv())

# todo 

# 1. crud.update_capture
# 2. stage and status update.
# 3. sum up the whole process 
class customTask(Task):
    def before_start(self, task_id, args, kwargs):
        update_capture_status(uuid=task_id,status=STATUS.PROCESSING)
        print(f"Task: {task_id},Status: {STATUS.PROCESSING}")

    def on_success(self, retval, task_id, args, kwargs):
        update_capture_status(uuid=task_id,status=STATUS.SUCCESS)
        print(f"Task: {task_id},Status: {STATUS.SUCCESS}")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        update_capture_status(uuid=task_id,status=STATUS.FAILURE)
        print(f"Task: {task_id},Status: {STATUS.FAILURE}")
    

colmap_app = Celery('colmap_app',  # The queue 
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/1',
             task_cls=customTask)

colmap_app.conf.broker_connection_retry_on_startup = True # 启动时重试连接

@colmap_app.task(bind=True) # bind=True 会将task(这里是customTask)实例作为第一个参数传入
def process(self,uuid):
    storage_dir = root_dir /Path(os.environ.get('STORAGE_DIR')) / uuid
    video_path = storage_dir / f"{uuid}.mp4"
    image_dir  = storage_dir / "input"
    convert_video_to_images(video_path=video_path, image_dir=image_dir,num_frames_target=300,num_downscales=1)
    convert_images_to_colmap(source_path=image_dir,verbose=False)
    try:
        pass
        # os.remove(video_path)
    except: 
        print(f"{video_path} does't exist")
    # todo: 修正照片质量

    


    

    
    
    
    

