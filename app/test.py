import redis 
import os 

host = "r-bp1slexehxv9ykg1y7pd.redis.rds.aliyuncs.com"
pwd ="u@@HkaK99GTi@Nq"
r = redis.Redis(host=host, port=6379,username="future", password=pwd)
print(r)
print(r.set('name1', 'chenge'))
