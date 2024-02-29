# -*- coding: utf-8 -*-
import oss2
import os 
from oss2.credentials import EnvironmentVariableCredentialsProvider
from dotenv import load_dotenv, find_dotenv
from pathlib import Path 
load_dotenv(find_dotenv("config.env"))
# 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录RAM控制台创建RAM账号。
endpoint = os.getenv("OSS_ENDPOINT")
bucket_name = os.getenv("OSS_BUCKET_NAME")
auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
service = oss2.Service(auth, endpoint=endpoint)
# 填写Bucket名称，例如examplebucket。
bucket = oss2.Bucket(auth, endpoint=endpoint, bucket_name='f-test-bucket')


def download_file(oss_key, local_path):
    """
    oss_key: 要下载的文件在OSS上的路径
    local_path: 本地文件保存路径,要求父目录存在，且有写权限
    """
    if not isinstance(local_path, str):
        local_path = str(local_path)
    try:
        bucket.get_object_to_file(oss_key, local_path)    
    except Exception as e:
        print(e)
        raise e 

def get_frame(video_path,image_path):
    if not isinstance(image_path, str):
        local_path = str(local_path)
    if not isinstance(video_path, str):
        video_path = str(video_path)

    try:
        subprocess.run(["ffmpeg",'-loglevel', 'error', "-i", video_path, "-ss", "00:00:59", "-vframes", "1", image_path])
    except Exception as e:
        print(e)
        raise e 

def upload_file(oss_key, local_path):
    """
    oss_key: 要上传的文件在OSS上的路径
    local_path: 本地文件路径,要求父目录存在，且有读权限
    """
    if not isinstance(local_path, str):
        local_path = str(local_path)
    try:
        bucket.put_object_from_file(oss_key, local_path)  
        return True  
    except Exception as e:
        print(e)
        raise e 
    
def delete_oss_file(oss_key):

    try:
        bucket.delete_object(oss_key)  
        return True  
    except Exception as e:
        print(e)
        raise e 

def delete_local_dir(local_dir):
    import shutil
    try:
        shutil.rmtree(local_dir) 
        return True 
    except Exception as e:
        print(e)
        raise e 

def prepare_job(uuid:str):
    """
    函数用于准备一个视频处理任务。具体步骤如下：

    1. 验证并处理输入的 uuid，确保其为字符串类型。
    2. 从环境变量中获取存储目录，并构造视频和图片的 OSS key。
    3. 在存储目录下创建一个以 uuid 命名的工作目录。
    4. 构造视频和图片的本地存储路径。
    5. 尝试执行以下操作：
       - 从 OSS 下载视频文件到本地工作目录。
       - 从视频文件中截取一帧并保存为图片。
       - 将图片上传到 OSS。
    6. 如果以上操作全部成功，返回 True；否则，打印异常信息并抛出异常。

    参数：
    uuid: str，唯一标识符，用于构造 OSS key 和本地文件路径。

    返回：
    bool，如果所有操作都成功，返回 True；否则，抛出异常。
    """
    if not isinstance(uuid, str):
        uuid = str(uuid)
    storage_dir = Path(os.getenv("STORAGE_DIR")) #相对于app目录
    file_name = uuid + ".mp4"
    oss_video_key = "video/" + file_name
    oss_image_key = "image/" + uuid + ".png"
    work_dir = storage_dir / uuid 
    work_dir.mkdir(parents=True, exist_ok=True)
    video_path = work_dir /file_name
    image_path = work_dir / (str(uuid) + ".png")
    
    try:
        download_file(oss_video_key, str(video_path))
        get_frame(video_path, str(image_path))
        upload_file(oss_image_key, str(image_path))
        return True 
    except Exception as e:
        print(e)
        raise e 

def get_oss_image_url(oss_image_key,expire=600):
    """
    获取 OSS 图片的 URL,用于分享。

    参数：
    oss_image_key: str，OSS 图片的路径。
    expire: int，URL 有效期，单位为秒。

    返回：
    str，OSS 图片的 URL。
    """
    if not isinstance(oss_image_key, str):
        oss_image_key = str(oss_image_key)
    url = "https://" + bucket_name + "." + endpoint + "/" + oss_image_key
    return url 
if __name__ == '__main__':
    import subprocess 
    oss_key = "video/"
    storage_dir = Path(os.getenv("STORAGE_DIR")) #相对于app目录
    uuid =  "5b78cb1f-92b2-4021-9f8a-a60e442d9e7d"
    file_name = uuid + ".mp4"
    oss_key = oss_key + file_name
    
    video_path = storage_dir / uuid / file_name

    video_path.parent.mkdir(parents=True, exist_ok=True)

    # if prepare_job(uuid):
    #     print("准备工作成功")
    # os.chmod(local_path.parent,os.stat(local_path.parent).st_mode | 0o777)

    # download_file(oss_key, rf"D:/Repo/webApp/app/storage/5b78cb1f-92b2-4021-9f8a-a60e442d9e7d/5b78cb1f-92b2-4021-9f8a-a60e442d9e7d.mp4")
    # download_file(oss_key, str(local_path))

    # 截图
    # image_path = video_path.parent / (uuid + ".png")

    # try:
    #     subprocess.run(["ffmpeg", "-i", video_path, "-ss", "00:00:59", "-vframes", "1", image_path])
    # except Exception as e:
    #     print(e)
    #     raise e 
    
    # 上传文件
    # oss_image_key = "image/" + uuid + ".png"
    # if upload_file(oss_image_key, image_path):
    #     print("上传成功")

    # 删除文件
    # if delete_oss_file(oss_image_key):
        # print("删除成功")
    delete_local_dir(video_path.parent)