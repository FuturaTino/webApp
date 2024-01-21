from celery import Celery
from celery import Task 
import time
from dotenv import load_dotenv
import os
from pathlib import Path
from process_image import convert_video_to_images,convert_images_to_colmap
import shutil 

load_dotenv('.env')

# todo 

# 1. crud.update_capture
# 2. stage and status update.
# 3. sum up the whole process 

class ProcessingTask(Task):
    def __init__(self):
        super().__init__()
    def before_start(self, task_id, args, kwargs):
        self.dir = Path(os.getenv('STORAGE_DIR'))  / task_id 
        if not self.dir.exists():
            self.dir.mkdir()

        
        
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        print('after_return')

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('on_failure')
        # crud.update_capture 
        shutil.rmtree(self.dir)
        raise exc
        
    
    def on_success(self, retval, task_id, args, kwargs):
        print('on_success')
        
colmap_app = Celery(__name__,  # The queue 
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/1',
             task_cls=ProcessingTask)

colmap_app.conf.broker_connection_retry_on_startup = True # 启动时重试连接

@colmap_app.task(bind=True) # bind=True 会将task(这里是customTask)实例作为第一个参数传入
def procressing(self,filepath:str):
    """
    Deal with veideo data to pre-processed colmap data
    """
    convert_video_to_images(filepath,self.dir)
    convert_images_to_colmap(self.dir)
    # crud.update_capture
    
    
    
    

