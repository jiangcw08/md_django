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

from .myser import CarouselSer,GoodsSer,CateSer

from myapp.models import User,Carousel,Goods,Category

from rest_framework.views import APIView,Response


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

        #检索字段
        text = request.GET.get('text',None)

        



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

        #是否进行模糊查询
        if text:

            text = json.loads(text)

            for item in text:

                print(item)
                goods = Goods.objects.filter(Q(name__contains=item) | Q(desc__contains=item))[data_start:data_end]

                count = Goods.objects.filter(Q(name__contains=item) | Q(desc__contains=item)).count()

        else:

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
