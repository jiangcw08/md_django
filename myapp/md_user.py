from mydjango.settings import BASE_DIR

from django.db.models import Q,F

from django.views import View
from PIL import Image,ImageFont,ImageDraw
from django.shortcuts import redirect
from dwebsocket.decorators import accept_websocket
import uuid
import hashlib
import re
import random
import io
import requests
import json


import os

from mydjango.settings import UPLOAD_ROOT

from django.http import HttpResponse


from myapp.models import User

from rest_framework.views import APIView,Response

#又拍云存储
import upyun
class UpYun(APIView):

    def post(self,request):

        #获取文件
        file = request.FILES.get('file')
        #新建又拍云实例
        up = upyun.UpYun('jiangcw-upyun','jiangcw','Tb5WxPjiIpklrG6heUZSwb15SnIQ5ETv')
        #声明头部信息
        headers = {'x-gmkerl-rotate':'auto'}
        #上传图片
        for chunk in file.chunks():
            res = up.put(file.name,chunk,checksum=True,headers=headers)
        return Response({'filename':file.name})


#获取用户信息
class UserInfo(APIView):

    def get(self,request):

        id = request.GET.get('id')
        user = User.objects.get(id=id)

        img = user.img

        return Response({'img':img})


#跟新头像
class UserImg(APIView):


    def put(self, request):
        id = request.data.pop('id')
        flag = User.objects.filter(id=id).update(**request.data)

        return Response({'message':'更新成功'})

#七牛云token
from qiniu import Auth

class QiNiu(APIView):
    def get(self,request):

        #声明认证
        q = Auth('avwXUyLRJ4ldXi4-b-160_Lf5Uaq_t5MGkBTVJAj','e-P6avQmYx5OXKVkkunYj_-5_nmkVaYmXQoYlhL3')

        #获取token
        token = q.upload_token('meidshop')

        return Response({'token':token})

#文件上传通用类
class UploadFile(APIView):

    def post(self,request):

        #接收参数
        myfile = request.FILES.get('file')
        uid = request.POST.get('uid')

        #建立文件流对象
        f = open(os.path.join(UPLOAD_ROOT,'',myfile.name.replace('"','')),'wb')
        #写入
        for chunk in myfile.chunks():
            f.write(chunk)
        f.close()

        #修改头像地址
        user = User.objects.get(id=uid)

        user.img = myfile.name.replace('"','')
        user.save()

        return Response({'filename':myfile.name.replace('"','')})


#新浪微博回调
def wb_black(request):

    code = request.GET.get('code',None)

    #定义token接口地址
    url = "https://api.weibo.com/oauth2/access_token"

    #获取token
    re = requests.post(url,data={

        "client_id":"518243583",
        "client_secret":"77b59cb73127e7e73f1f6d81972a6647",
        "grant_type":"authorization_code",
        "code":code,
        "redirect_uri":"http://127.0.0.1:8000/sina_weibo"


    })
    # print(re.json())

    #token换取新浪微博用户信息
    res = requests.get('https://api.weibo.com/2/users/show.json',params={'access_token':re.json()['access_token'],'uid':re.json()['uid']})

    res = json.loads(res.text)
    print(res)

    sina_name = ''
    user_id = ''

    #判断是否用新浪登录过
    user = User.objects.filter(username=res['name']).first()
    if user:
        sina_name = user.username
        user_id = user.id
    else:
        #没登录过，自动创建账号
        user = User(username=str(res['name']),password='',)
        user.save()
        sina_name = res['name']

        #查询用户id

        user = User.objects.filter(username=str(res['name'])).first()

        user_id = user.id

    #跳转到vue首页 
    return redirect('http://localhost:8080?sina_name='+str(sina_name)+'&uid='+str(user_id))


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
        code = request.GET.get('code')
        username = request.GET.get('username')
        password = request.GET.get('password')
        phone = request.GET.get('phone')

        redis_code = r.get('code').decode('utf-8')
        if code != redis_code:
            return Response({'code':403,'message':'请输入正确的验证码'})


        #排重
        user = User.objects.filter(username=username).first()
        if user:
            res = {}
            res['code'] = 400
            res['message'] = '该用户名可不用'
            return Response(res)
        else:
            user = User(username=username,password=make_password(password),phone=phone)
            user.save()
            res = {}
            res['code'] = 200
            res['message'] = '注册成功'
            return Response(res)


#登录
class Login(APIView):

    def get(self,request):


        username = request.GET.get('username',None)
        passowrd = request.GET.get('password',None)
        code = request.GET.get('code',None)

        redis_code = r.get('code').decode('utf-8')
        #session中取值
        # session_code = request.session.get('code',None)
        # print(session_code)

        if code != redis_code:
            return Response({'code':403,'message':'请输入正确的验证码'})


        # r.lpop(username)
        print(r.llen(username))
        if r.llen(username) < 3:
            user = User.objects.filter(username=username,password=make_password(passowrd)).first()
            
            if user:

                return Response({'code':200,'message':'登录成功','uid':user.id,'username':user.username})

            else:

                r.lpush(username,1)
                r.expire(username,20)

                num = 3-r.llen(username)
                if num > 0:
                    return Response({'code':403,'message':'用户名或密码错误,还可以尝试%s次'%(3-r.llen(username))})
 
                else:
                    return Response({'code':403,'message':'您的账号已被锁定'})
        else:
            return Response({'code':403,'message':'您的账号已被锁定'})

        
   

        
    


#导包
import redis

#定义ip端口
host = 'localhost'
port = '6379'


#建立链接
r = redis.Redis(host=host,port=port)


#自定义图片验证码
class MyCode(View):

    #定义rgb随机颜色
    def get_random_color(self):

        R = random.randrange(255)
        G = random.randrange(255)
        B = random.randrange(255)

        return (R,G,B)
    #定义图片
    def get(self,request):
        #画布
        img_size = (150,75)
        #定义图片对象
        image = Image.new('RGB',img_size,'white')
        #定义画笔
        draw = ImageDraw.Draw(image,'RGB')
        source = '0987654321qwertyuioplkjhgfdsazxcvbnm'
        #接收容器
        code_str = ''
        #定义字体
        my_font = ImageFont.truetype(font="c:\\Windows\\Fonts\\LeelawUI.ttf",size=18)

        for i in range(4):
            #获取字母颜色
            text_color = self.get_random_color()
            #获取随机下标
            tmp_num = random.randrange(len(source))
            #随机字符串
            random_str = source[tmp_num]
            #装入容器
            code_str += random_str
            #绘制字符串
            draw.text((25+30*i,26),random_str,text_color,font=my_font)

        #建立缓存区
        buf = io.BytesIO()
        #将临时图片保存到缓存区
        image.save(buf,'png')
        #保存随机码
        r.set('code',code_str)
        #保存session
        # request.session['code'] = code_str
        # print(r.get('code').decode('utf-8'))

        return HttpResponse(buf.getvalue(),'image/png')


        
        

