"""mydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from django.views.static import serve
from myapp.views import myindex
from myapp.md_user import Register,Login,MyCode,wb_black,UploadFile,QiNiu,UserImg,UserInfo,UpYun,GetCarousel,Userlist
from myapp.kaoshi import Get_goods
from myapp.md_goods import InsertGoods,CateList,Goodslist,GoodInfo,Sarch,CommentInsert,CommentList,Reply
urlpatterns = [
    #定义超链接路由
    re_path('^static/upload/(?P<path>.*)$',serve,{'document_root':'/static/upload/'}),
    path('',myindex),
    path('register/',Register.as_view()),
    path('login/',Login.as_view()),
    path('code/',MyCode.as_view()),
    path('sina_weibo',wb_black),
    path('file/',UploadFile.as_view()),
    path('qn/',QiNiu.as_view()),
    path('userimg/',UserImg.as_view()),
    path('userinfo/',UserInfo.as_view()),
    path('upyun/',UpYun.as_view()),
    path('getcaroule/',GetCarousel.as_view()),
    path('insertgoods/',InsertGoods.as_view()),
    path('catelist/',CateList.as_view()),
    path('goodslist/',Goodslist.as_view()),
    path('goodinfo/',GoodInfo.as_view()),
    path('sarch/',Sarch.as_view()),
    path('kaoshi/',Get_goods.as_view()),
    path('addcomment/',CommentInsert.as_view()),
    path('commentlist/',CommentList.as_view()),
    path('userlist/',Userlist.as_view()),
    path('reply/',Reply.as_view())

    
]
