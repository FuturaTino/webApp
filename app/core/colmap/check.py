import subprocess
from subprocess import PIPE
def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=PIPE, stderr=PIPE)
        return True
    except FileNotFoundError:
        return False 

def check_colmap():
    try:
        subprocess.run(['colmap', '--help'], stdout=PIPE, stderr=PIPE)
        return True
    except FileNotFoundError:
        return False

def check_install():
    meta = {
        'ffmpeg': check_ffmpeg(),
        'colmap': check_colmap() 
    }
    if check_ffmpeg() and check_colmap():
        return True
    else:
        return meta

if __name__ == '__main__':
    from colmap_app import process,colmap_app
    uuid = '2f43fef3-b3e1-440c-b9de-7c269970e639'
    process.apply_async((uuid,),task_id=uuid)