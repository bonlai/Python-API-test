from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name')

class ProfilePicSerializer(serializers.HyperlinkedModelSerializer):
    image=serializers.ImageField(max_length=None,use_url=True)
    #user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Profile
        fields = ('image','user_id')

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    #user = UserSerializer()
    #url = serializers.HyperlinkedIdentityField(view_name="API:profile-detail")
    '''
        url = serializers.HyperlinkedIdentityField(
        view_name='profile-detail',
        lookup_field='user_id'
    )
    '''
    #image=serializers.ImageField(max_length=None,use_url=True)
    class Meta:
        model = Profile
        fields = ('dob','location','gender','self_introduction','user_id')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            ProfilePic.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
        instance.profilepic.save()

'''
class AppUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AppUser
        fields = '__all__'
'''

class RestaurantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantImage
        fields = '__all__'

class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class ParticipateSerializer(serializers.ModelSerializer):
    '''
    gathering = serializers.HyperlinkedRelatedField(
        queryset=Gathering.objects.all(),
        view_name='gathering-detail'
    )
    '''
    class Meta:
        model = Participate
        fields = ('user','gathering')



class GatheringSerializer(serializers.ModelSerializer):
    '''
    created_by_id=serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail',
    )
    '''
    #created_by= UserSerializer(read_only=False)
    #restaurant_id=RestaurantSerializer(read_only=False)
   # member=UserSerializer();
    class Meta:
        model = Gathering
        #fields = '__all__'
        fields = ('id','name','start_datetime','is_start','created_by','restaurant','member')

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'                

      
