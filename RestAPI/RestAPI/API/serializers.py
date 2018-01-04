from rest_framework import serializers
from .models import Image,ProfilePic,AppUser


class ImagesSerializer(serializers.HyperlinkedModelSerializer):
    image=serializers.ImageField(max_length=None,use_url=True)
    class Meta:
        model = Image
        fields = ('id', 'image', 'url')

class ProfilePicSerializer(serializers.HyperlinkedModelSerializer):
    image=serializers.ImageField(max_length=None,use_url=True)
    class Meta:
        model = ProfilePic
        fields = ('id', 'image', 'url')

class AppUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AppUser
        fields = '__all__'
        