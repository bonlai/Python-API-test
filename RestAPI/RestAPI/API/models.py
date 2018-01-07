from django.db import models
from django.db.models.fields.related import ForeignKey
#from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.contrib.auth.models import User
#from django.conf import settings

class ProfilePic(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to='ProfilePic/', default='Images/None/No-img.jpg')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class Meta:
        db_table = "profilePic"

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True)
    self_introduction = models.TextField(blank=True)
    location = models.CharField(max_length=30, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6)
    self_introduction = models.TextField(blank=True)
    class Meta:
        db_table = "profile"

'''
class AppUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(null=True)
    #phone = models.CharField(max_length=20, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6)
    address = models.TextField(blank=True)
    self_introduction = models.TextField(blank=True)
    password = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    profilePic=models.ForeignKey('profilePic',null=True, blank=True);

    class Meta:
        db_table = "appUser"
'''

class Interest(models.Model):
    name = models.CharField(max_length=10)
    #user=models.ForeignKey('AppUser');
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "interest"

class Gathering(models.Model):
    name = models.CharField(max_length=100)
    details = models.TextField()
    start_datetime = models.DateTimeField()
    is_start=models.BooleanField()
    #created_by = models.ForeignKey('appUser')
    created_by = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant=models.ForeignKey('restaurant')
    #participate=models.ForeignKey('participate')
    #member=models.ManyToManyField(AppUser, through='participate',related_name ='joined')

    class Meta:
        db_table = "gathering"

class Participate(models.Model):
    gathering=models.ForeignKey(Gathering, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    joined_datetime = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    class Meta:
        db_table = "participate"

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    #phone = models.CharField(max_length=20, null=True)
    address = models.TextField()
    category = models.CharField(max_length=30)
    #created = models.DateTimeField(auto_now_add=True)
    average_rate=models.FloatField(blank=True,null=True)
    review_count=models.IntegerField(blank=True,null=True)
    #image=models.ForeignKey('images');

    class Meta:
        db_table = "restaurant"

class Review(models.Model):
    comment=models.TextField()
    rating=models.IntegerField()
    created_by = models.ForeignKey(User)
    restaurant=models.ForeignKey('restaurant')

    class Meta:
        db_table = "review"

class RestaurantImage(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to='RestaurantImage/', default='Images/None/No-img.jpg')
    restaurant=models.ForeignKey('restaurant')
    class Meta:
        db_table = "restaurantImage"

class OtherInfo(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    restaurant=models.ForeignKey('restaurant')

    class Meta:
        db_table = "otherInfo"