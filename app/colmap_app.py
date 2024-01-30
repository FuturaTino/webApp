from celery import Celery
from celery import Task 
import time
from dotenv import load_dotenv,find_dotenv
import os
from pathlib import Path
import shutil 
from core.colmap.convert import convert_video_to_images,convert_images_to_colmap
from core.dependencies import get_db

from crud.captures import update_capture_status,STATUS

load_dotenv(find_dotenv())
root_dir = Path(__file__).parent # app dir

class customTask(Task):
    def before_start(self, task_id, args, kwargs):
        update_capture_status(db=next(get_db()),uuid=task_id,status=STATUS['PreProcessing'])
        print(f"Task: {task_id},Status: {STATUS['PreProcessing']}")

    def on_success(self, retval, task_id, args, kwargs):
        update_capture_status(db=next(get_db()),uuid=task_id,status=STATUS['Success'])
        print(f"Task: {task_id},Status: {STATUS['Success']}")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        update_capture_status(db=next(get_db()),uuid=task_id,status=STATUS['Failed'])
        print(f"Task: {task_id},Status: {STATUS['Failed']}")
    

colmap_app = Celery('colmap_app',  # The queue 
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/1',
             task_cls=customTask)

colmap_app.conf.broker_connection_retry_on_startup = True # 启动时重试连接'


@colmap_app.task(bind=True,time_limit=60*60) # bind=True 会将task(这里是customTask)实例作为第一个参数传入
def process(self,uuid):

    storage_dir = root_dir / Path(os.environ.get('STORAGE_DIR')) / uuid
    video_path:Path = storage_dir / f"{uuid}.mp4"
    if not video_path.exists():
        raise Exception(f"{video_path} does't exist")
    
    image_dir  = root_dir / storage_dir / "input"
    convert_video_to_images(video_path=video_path, image_dir=image_dir,num_frames_target=300,num_downscales=1)
    convert_images_to_colmap(source_path=storage_dir,verbose=False)
    try:
        pass
        # os.remove(video_path)
    except: 
        print(f"{video_path} does't exist")
    # todo: 修正照片质量

if __name__ == '__main__':
    colmap_app.start()

    


    

    
    
    
    

