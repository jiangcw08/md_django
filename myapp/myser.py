from rest_framework import serializers

from myapp.models import Carousel,Goods,Category,Comment,User

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

class CommentSer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"    

class UserSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"