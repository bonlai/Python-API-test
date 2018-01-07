from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username')

class ProfilePicSerializer(serializers.HyperlinkedModelSerializer):
    image=serializers.ImageField(max_length=None,use_url=True)
    class Meta:
        model = ProfilePic
        fields = '__all__'

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    #user = UserSerializer()
    class Meta:
        model = Profile
        fields = ('url','dob','location','gender','self_introduction')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

'''
class AppUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AppUser
        fields = '__all__'
'''
class GatheringSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Gathering
        fields = '__all__'

class RestaurantImageSerializer(serializers.HyperlinkedModelSerializer):
    image=serializers.ImageField(max_length=None,use_url=True)
    class Meta:
        model = RestaurantImage
        fields = '__all__'
        

      
