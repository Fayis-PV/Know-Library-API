from rest_framework import serializers
from .models import Website,Category
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .fields import ImageUrlField

# Create Serializers here

class WebsiteSerializer(serializers.ModelSerializer):
    image = ImageUrlField(allow_null = True,)
    banners = ImageUrlField(allow_null = True)
    class Meta:
        model = Website
        fields = ['id','name','description','url','image','banners','category','active']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length = 128,write_only = True)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.username
        return token