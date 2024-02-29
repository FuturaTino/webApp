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
from core.oss import upload_file,prepare_job,delete_local_dir
from core.reconstruct.train import training

from crud.captures import update_capture_status,STATUS


load_dotenv(find_dotenv("config.env"))
username = os.environ.get("REDIS_USER")
password = os.environ.get("REDIS_PASSWORD")
host = os.environ.get("REDIS_HOST")
port = os.environ.get("REDIS_PORT")

app = Celery(__name__,  
             broker=f'redis://{username}:{password}@{host}:{port}/0',
             backend=f'redis://{username}:{password}@{host}:{port}/1')


# celery settings from https://docs.celeryq.dev/en/stable/userguide/configuration.html
app.conf.broker_connection_retry_on_startup = True
# About routes https://docs.celeryq.dev/en/stable/userguide/routing.html
# app.conf.task_default_exchange = 'default'
# app.conf.task_default_queue = 'default'
app.conf.task_default_exchange_type = 'fanout' # 广播模式
app.conf.task_queues = (
    Queue('colmap', routing_key='colmap.low'), # exchange:实体交换机 ；交换机中的routing_key 永远区分 一个celery中的多个队列（优先级）
    Queue('gs', routing_key='gs.low')
)

class colmapTask(Task):
    def __init__(self) -> None:
        root_dir = Path(__file__).parent # app dir
        self.sotrage_dir = root_dir / Path(os.environ.get('STORAGE_DIR'))   

    def before_start(self, task_id, args, kwargs):

        update_capture_status(db=next(get_db()),uuid=task_id,status=STATUS['PreProcessing'])
        try:
            prepare_job(uuid=task_id)
            print(f"Task: {task_id},Status: {STATUS['PreProcessing']}")
        except Exception as e:
            update_capture_status(db=next(get_db()),uuid=task_id,status=STATUS['Failed'])
            print(f"Task: {task_id},Status: {STATUS['Failed']}")
            raise e

    def on_success(self, retval, task_id, args, kwargs):
        update_capture_status(db=next(get_db()),uuid=task_id,status=STATUS['Queue_2'])
        print(f"Task: {task_id},Status: {STATUS['Queue_2']} ✅💨 ")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        update_capture_status(db=next(get_db()),uuid=task_id,status=STATUS['Failed'])
        print(f"Task: {task_id},Status: {STATUS['Failed']}")
    
class gsTask(Task):
    def __init__(self) -> None:
        root_dir = Path(__file__).parent # app dir
        self.sotrage_dir = root_dir / Path(os.environ.get('STORAGE_DIR'))  

    def before_start(self, task_id, args, kwargs):
        update_capture_status(db=next(get_db()),uuid=task_id,status=STATUS['Reconstructing'])
        print(f"Task: {task_id},Status: {STATUS['Reconstructing']}")

    def on_success(self, retval, task_id, args, kwargs):
        try:
            work_dir = Path(os.getenv('STORAGE_DIR')) / task_id
            delete_local_dir(work_dir)
            update_capture_status(db=next(get_db()),uuid=task_id,status=STATUS['Success'])
            print(f"Task: {task_id},Status: {STATUS['Success']} ✅ ")
        except Exception as e:
            update_capture_status(db=next(get_db()),uuid=task_id,status=STATUS['Failed'])
            raise e
        
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        update_capture_status(db=next(get_db()),uuid=task_id,status=STATUS['Failed'])
        print(f"Task: {task_id},Status: {STATUS['Failed']}")

@app.task(bind=True, time_limit=60*60,base=colmapTask) # bind=True 会将task(这里是customTask)实例作为第一个参数传入
def process(self,uuid):
    pass
@app.task(bind=True, time_limit=60*60,base=gsTask)
def reconstruct(self,uuid):
    pass
    

    
    
    
    

