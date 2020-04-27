#导包
import redis

#定义ip端口
host = 'localhost'
port = '6379'


#建立链接
r = redis.Redis(host=host,port=port)

#字符串的使用
# r.set('test','hellow word')

# #取值 转码
# code = r.get('test').decode('utf-8')

# print(code)
r.lpush('123',1)
print(r.llen('123'))