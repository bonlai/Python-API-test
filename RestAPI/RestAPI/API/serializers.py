from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import *
from rest_framework.validators import UniqueTogetherValidator
from API.recommendation import *

class ProfilePicSerializer(serializers.HyperlinkedModelSerializer):
    image=serializers.ImageField(max_length=None,use_url=True)
    class Meta:
        model = Profile
        fields = ('user_id','image')

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    image=serializers.ImageField(max_length=None,use_url=True,read_only=True)
    class Meta:
        model = Profile
        fields = ('user_id','dob','location','gender','self_introduction','image')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            ProfilePic.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

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
    image = RestaurantImageSerializer(many=True, read_only=True)
    class Meta:
        model = Restaurant
        fields = ('id','name','image','address','category','average_rate','review_count')

class ParticipateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True) 
    class Meta:
        model = Participate
        fields = ('id','user','gathering')

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendedRate
        fields = ('rating',)

class GatheringSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True) 

    #recommend=RateSerializer(many=True, read_only=True)
    class Meta:
        model = Gathering
        #fields = '__all__'
        fields = ('id','name','details','start_datetime','is_start','user','restaurant','member')
    '''def get_recommended_rate(self, obj):
        requestuser =  self.context['request'].user
        requestrestaurant=obj.restaurant
        s=SlopeOne()
        print(requestuser.id)
       # if(Review.objects.get(user=requestuser,restaurant=requestrestaurant))
        value=s.predict(requestuser.id,requestrestaurant.id)     
        c=RecommendedRate(restaurant=requestrestaurant,user=requestuser,rating=value)
        c.save()
        return value'''

class RestaurantLocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('address',)

class GatheringLocationSerializer(serializers.ModelSerializer):
    restaurant = RestaurantLocationSerializer()
    class Meta:
        model = Gathering
        fields = ('id','name','restaurant')

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ('id','name',)

class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username')

class ReviewSerializer(serializers.ModelSerializer):
    #user = serializers.PrimaryKeyRelatedField(read_only=True) 
    user=UsernameSerializer(read_only=True,required=False, allow_null=True)
    class Meta:
        model = Review
        fields = ('id','user','comment','rating','restaurant')


class LatLongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('latitude','longitude')      
