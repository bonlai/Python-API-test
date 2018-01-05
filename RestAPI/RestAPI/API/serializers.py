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