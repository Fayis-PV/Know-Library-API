from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files import File
from urllib.request import urlopen
from io import BytesIO

# Create Serializers here


class ImageUrlField(serializers.FileField):
    def to_internal_value(self, data): 
        if data is None:
            return None 
        elif not isinstance(data,File):
            return data
        return super().to_internal_value(data)


class WebsiteSerializer(serializers.ModelSerializer):
    image = ImageUrlField(allow_null = True)
    banners = ImageUrlField(allow_null = True)
    class Meta:
        model = Website
        fields = ['id','name','description','url','image','banners','category','active']

    def validate_image(self,value):
        return value

    def to_internal_value(self, instance):
        data =  super().to_internal_value(instance)
        category = data.pop('category',[])
        return data


    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AdminAuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length = 128,write_only = True)
