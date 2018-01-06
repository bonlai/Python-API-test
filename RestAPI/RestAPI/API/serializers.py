from rest_framework import serializers
from .models import *



class ProfilePicSerializer(serializers.HyperlinkedModelSerializer):
    image=serializers.ImageField(max_length=None,use_url=True)
    class Meta:
        model = ProfilePic
        fields = ('id', 'image', 'url')

class AppUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AppUser
        fields = '__all__'

class GatheringSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Gathering
        fields = '__all__'

class RestaurantImageSerializer(serializers.HyperlinkedModelSerializer):
    image=serializers.ImageField(max_length=None,use_url=True)
    class Meta:
        model = RestaurantImage
        fields = ('id', 'image', 'url')
        
from django.contrib.auth.models import User
from rest_framework import permissions
from django.contrib.auth import get_user_model

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    #images  = serializers.PrimaryKeyRelatedField(many=True, queryset=Img.objects.all())
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

        
    class Meta:
        model = User
        fields = ('username','password')