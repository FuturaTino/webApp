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
    print(check_install())