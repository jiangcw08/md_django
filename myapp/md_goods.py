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
