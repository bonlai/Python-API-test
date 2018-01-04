from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class Image(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to='Image/', default='Images/None/No-img.jpg')

    class Meta:
        db_table = "image"

class ProfilePic(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to='ProfilePic/', default='Images/None/No-img.jpg')

    class Meta:
        db_table = "profilePic"

class RestaurantImage(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to='RestaurantImage/', default='Images/None/No-img.jpg')

    class Meta:
        db_table = "restaurantImage"

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
)

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

class Interest(models.Model):
    name = models.CharField(max_length=10)
    user=models.ForeignKey('AppUser');

    class Meta:
        db_table = "interest"

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, null=True)
    address = models.TextField()
    self_introduction = models.TextField()
    password = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    #image=models.ForeignKey('images');

    class Meta:
        db_table = "restaurant"

class Gathering(models.Model):
    name = models.CharField(max_length=100)
    details = models.TextField()
    start_datetime = models.DateTimeField()
    is_start=models.BooleanField()
    #created_by = models.ForeignKey('appUser')
    restaurant=models.ForeignKey('restaurant')
    #participate=models.ForeignKey('participate')
    member=models.ManyToManyField(AppUser, through='participate')

    class Meta:
        db_table = "gathering"

class Participate(models.Model):
    gathering=models.ForeignKey(Gathering, on_delete=models.CASCADE)
    user=models.ForeignKey(AppUser, on_delete=models.CASCADE)
    joined_datetime = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    class Meta:
        db_table = "participate"

class OtherInfo(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    restaurant=models.ForeignKey('restaurant')

    class Meta:
        db_table = "otherInfo"

class Review(models.Model):
    comment=models.TextField()
    rating=models.IntegerField()
    created_by = models.ForeignKey('appUser')
    restaurant=models.ForeignKey('restaurant')

    class Meta:
        db_table = "gathering"