import jwt
import datetime

#载荷中加入生命周期概念
playload = {
    'exp' : int((datetime.datetime.now() + datetime.timedelta(seconds=30)).timestamp()),
    'data':{'uid':2}
    
}

#生成jwt

encode_jwt = jwt.encode(playload,'qwe123',algorithm="HS256")

# print((encode_jwt).decode('utf-8'))

encode_str = str(encode_jwt,'utf-8')
# print(encode_str)
try:
    decode_jwt = jwt.decode(encode_str,'qwe123',algorithms=['HS256'])
except Exception as e:
    print('123')
    pass