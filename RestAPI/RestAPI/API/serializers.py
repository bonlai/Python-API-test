from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import *
from rest_framework.validators import UniqueTogetherValidator

class ProfilePicSerializer(serializers.HyperlinkedModelSerializer):
    image=serializers.ImageField(max_length=None,use_url=True)
    class Meta:
        model = Profile
        fields = ('user_id','image')

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('user_id','dob','location','gender','self_introduction',)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            ProfilePic.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
        instance.profilepic.save()

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','profile')
        
class RestaurantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantImage
        fields = '__all__'

class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class ParticipateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True) 
    class Meta:
        model = Participate
        fields = ('id','user','gathering')

class GatheringSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True) 
    class Meta:
        model = Gathering
        #fields = '__all__'
        fields = ('id','name','start_datetime','is_start','user','restaurant','member')


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True) 
    class Meta:
        model = Review
        fields = '__all__'                

      
