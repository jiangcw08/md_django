from rest_framework import serializers

from myapp.models import Carousel

#建立序列化类
class CarouselSer(serializers.ModelSerializer):

    class Meta:
        model = Carousel
        fields = "__all__"
        
         