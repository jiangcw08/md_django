from mydjango.settings import BASE_DIR

from django.db.models import Q,F

from django.views import View
from PIL import Image,ImageFont,ImageDraw

from dwebsocket.decorators import accept_websocket
import uuid
import hashlib
import re
import random
import io

from django.http import HttpResponse


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


        
        

