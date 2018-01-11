from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *

from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from rest_framework import generics
#from django.views.decorators.csrf import csrf_exempt

class ProfilePicViewSet(viewsets.ModelViewSet):
    queryset = ProfilePic.objects.all()
    serializer_class = ProfilePicSerializer
    #permission_classes = (IsAuthenticated,)

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class RestaurantImageViewSet(viewsets.ModelViewSet):
    queryset = RestaurantImage.objects.all()
    serializer_class = RestaurantImageSerializer
'''
class AppUserViewSet(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    #permission_classes = (IsAuthenticated,)

    @list_route(methods=['get'])
    def testing(self,request):
        serializer_context = {
            'request': request,
        }
        appUser = AppUser.objects.get(pk=2)
        serializer = AppUserSerializer(appUser,context=serializer_context)
        return Response(serializer.data)
'''
class GatheringViewSet(viewsets.ModelViewSet):
    queryset = Gathering.objects.all()
    serializer_class = GatheringSerializer

class ParticipateViewSet(viewsets.ModelViewSet):
    queryset = Participate.objects.all()
    serializer_class = ParticipateSerializer

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter