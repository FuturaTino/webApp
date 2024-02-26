# -*- coding: utf-8 -*-
import oss2
import os 
from oss2.credentials import EnvironmentVariableCredentialsProvider

# 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录RAM控制台创建RAM账号。
endpoint = os.getenv("OSS_ENDPOINT")
bucket_name = os.getenv("OSS_BUCKET_NAME")
auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
service = oss2.Service(auth, endpoint=endpoint)
# 填写Bucket名称，例如examplebucket。
bucket = oss2.Bucket(auth, endpoint=endpoint, bucket_name='f-test-bucket')

a = bucket.get_object_to_file('38bfe0fa-d611-478b-8d51-6186a95707ef.zip', fr'38bfe0fa-d611-478b-8d51-6186a95707ef.zip')
print(a)
b = bucket.get_object_to_file('zhangsan-eraLi-133757.mp4', fr'zhangsan-eraLi-133757.mp4')     

print(b)