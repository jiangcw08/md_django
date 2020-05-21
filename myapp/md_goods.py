from mydjango.settings import BASE_DIR

from django.db.models import Q,F

from django.utils.deprecation import MiddlewareMixin
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
import jwt
import datetime

import os

from mydjango.settings import UPLOAD_ROOT

from django.http import HttpResponse

from .myser import CarouselSer,GoodsSer,CateSer,CommentSer

from myapp.models import User,Carousel,Goods,Category,Comment

from rest_framework.views import APIView,Response



#商品评论回复
class Reply(APIView):

    def get(self, request):

        #接收参数
        content = request.GET.get('content')
        id = request.GET.get('id')
        username = request.GET.get('username')


        #查询被回复的评论
        comment = Comment.objects.get(id=id)

        my_list = []
        #查看是否存在评论回复
        if comment.reply:
            my_list = eval(comment.reply)
            my_list.insert(0,{'username':username,'content':content})
        else:
            my_list.insert(0,{'username':username,'content':content})
        

        comment.reply = json.dumps(my_list,ensure_ascii=False)
        # print(json.dumps(my_list,ensure_ascii=False))
        comment.save()

        return Response({'code':200})

        

            

        






#获取商品评论
class CommentList(APIView):

    def get(self,request):

        gid = request.GET.get('gid')

        comment = Comment.objects.filter(gid=gid).order_by("-id")

        comment_ser = CommentSer(comment,many=True)

        return Response(comment_ser.data)


#评论
import redis
#定义地址和端口
host = '127.0.0.1'
port = 6379
#建立redis连接
r = redis.Redis(host=host,port=port)

class CommentInsert(APIView):


    def post(self,request):

        id = request.POST.get('uid')
        uid = str(id)
        
        if r.llen(uid) > 2:
            return Response({'code':403,'message':'xieyixie'})

        print(request.data)

        comment = CommentSer(data=request.data)

        if comment.is_valid():
            
            comment.save()

            r.lpush(uid,1)
            r.expire(uid,5)

        return Response({'code':200,'message':'ok'})


# 格式化结果集
def dictfetch(cursor):

    # 声明描述符
    desc = cursor.description

    return [ dict(zip( [col[0] for col in desc],row)) 
            for row in cursor.fetchall()
    ]


#导入原生sql模块
from django.db import connection
# 搜索接口
class Sarch(APIView):
    def get(self,request):

        # 检索字段
        text = request.GET.get('text',None)
        
        # # 转换数据类型
        text = json.loads(text)

        #动态拼接
        sql = ''
        for val in text:

            sql += "or name like '%%%s%%'" % val
        sql = sql.strip('or')

        sql_cursor = "select id,name,price,img from goods where id != 0 and (" + sql + ")"

        print(sql_cursor)
        print('=========================')

        # 建立游标对象
        cursor = connection.cursor()

        # 执行sql语句
        cursor.execute(sql_cursor)
 
        # 查询
        # result  = cursor.fetchall()
        result = dictfetch(cursor)
        print(result)

        return Response({'data':result})


#商品详情
class GoodInfo(APIView):
    def get(self,request):

        id = request.GET.get('id')

        good = Goods.objects.get(id=id)

        good_ser = GoodsSer(good)

        return Response(good_ser.data)

#商品列表
class Goodslist(APIView):
    def get(self,request):


        basis = request.GET.get('basis','')
        kind = request.GET.get('kind','')

        #获取当前页
        page = request.GET.get('page',1)
        #一页显示个数
        size = request.GET.get('size',2)
        #计算从哪切
        data_start = (int(page)-1) * int(size)
        #计算切到哪
        data_end = int(page) * int(size)

        
        if basis:
            if kind:
                goods = Goods.objects.all().order_by(kind+basis)[data_start:data_end]
            else:
                goods = Goods.objects.all().order_by(basis)[data_start:data_end]
        #查询 切片操作
        else:
            goods = Goods.objects.all()[data_start:data_end]

        #查询所有商品个数
            count = Goods.objects.count()

        goods_ser = GoodsSer(goods,many=True)

        res = {}
        res['total'] = count
        res['data'] = goods_ser.data

        return Response(res)


#商品入库
class InsertGoods(APIView):
    def post(self, request):
        name = request.data.get('name')
        # 用户名重复性 校验
        good = Goods.objects.filter(name=name).first()
        if good:
            return Response({'code': 201,'message': '该商品已存在'})
        # 入库
        ser = GoodsSer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({'code':200,'message':'添加成功'})
        return Response({'code':400,'message':ser.errors})


#商品分类
class CateList(APIView):

    def get(self,request):

        cate = Category.objects.all()

        cate_ser = CateSer(cate,many=True)

        return Response(cate_ser.data)
