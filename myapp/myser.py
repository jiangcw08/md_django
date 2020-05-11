from rest_framework import serializers

from myapp.models import Carousel,Goods,Category

#建立序列化类
class CarouselSer(serializers.ModelSerializer):

    class Meta:
        model = Carousel
        fields = "__all__"
        
         
class GoodsSer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = "__all__"
        
class CateSer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"    