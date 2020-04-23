from mydjango.settings import BASE_DIR

from django.db.models import Q,F


from dwebsocket.decorators import accept_websocket
import uuid
import hashlib
import re
from myapp.models import User

from rest_framework.views import APIView,Response

#MD5加密方法
def make_password(mypass):

    #生成md5对象
    md5 = hashlib.md5()

    #转码
    mypass_utf8 = str(mypass).encode(encoding="utf-8")

    #加密
    md5.update(mypass_utf8)

    #返回密文
    return md5.hexdigest()

#注册

class Register(APIView):

    def get(self,request):

        username = request.GET.get('username')
        password = request.GET.get('password')
        phone = request.GET.get('phone')


        #排重
        user = User.objects.filter(username=username).first()
        if user:
            res = {}
            res['code'] = 400
            res['message'] = '该用户名可不用'
            return Response(res)
        else:
            user = User(username=username,password=password,phone=phone)
            user.save()
            res = {}
            res['code'] = 200
            res['message'] = '注册成功'
            return Response(res)




        

        

