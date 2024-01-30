from celery import Celery
from celery import Task 
import time
from dotenv import load_dotenv,find_dotenv
import os
from pathlib import Path
import shutil 
from core.dependencies import get_db

from crud.captures import update_capture_status,STATUS

load_dotenv(find_dotenv())
root_dir = Path(__file__).parent # app dir

class customTask(Task):
    def before_start(self, task_id, args, kwargs):
        update_capture_status(db=next(get_db()),uuid=task_id,status=STATUS['Reconstructing'])
        print(f"Task: {task_id},Status: {STATUS['Reconstructing']}")

    def on_success(self, retval, task_id, args, kwargs):
        update_capture_status(db=next(get_db()),uuid=task_id,status=STATUS['Success'])
        print(f"Task: {task_id},Status: {STATUS['Success']}")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        update_capture_status(db=next(get_db()),uuid=task_id,status=STATUS['Failed'])
        print(f"Task: {task_id},Status: {STATUS['Failed']}")
    

colmap_app = Celery('3dgs_app',  # The queue 
             broker='redis://localhost:6379/3',
             backend='redis://localhost:6379/4',
             task_cls=customTask)

colmap_app.conf.broker_connection_retry_on_startup = True # 启动时重试连接'


@colmap_app.task(bind=True,time_limit=60*60) # bind=True 会将task(这里是customTask)实例作为第一个参数传入
def reconstruct(self,uuid):

    storage_dir = root_dir / Path(os.environ.get('STORAGE_DIR')) / uuid

    pass 
    try:
        pass
        # os.remove(video_path)
    except: 
        pass 


if __name__ == '__main__':
    pass 

    


    

    
    
    
    

