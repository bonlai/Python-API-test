from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *

from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
#from rest_framework import filters
from django_filters import rest_framework as filters

from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
#from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException

class ListUser(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('id', 'username')
    #filter_fields = ('first_name',)

class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = ('id', 'username')

#will be discarded
class ProfilePicUpdate(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfilePicSerializer
    #permission_classes = (IsAuthenticated,)

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    #http_method_names = ['get', 'post', 'head']

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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    def perform_create(self, serializer):
        # Include the owner attribute directly, rather than from request data.
        instance = serializer.save(user=self.request.user)

class UserGatheringList(generics.ListAPIView):
    model = Gathering
    queryset = Gathering.objects.all()
    serializer_class = GatheringSerializer

    def get_queryset(self):
        id = self.kwargs['userid']
        return Gathering.objects.filter(user__id=id)


class ParticipateViewSet(viewsets.ModelViewSet):
    queryset = Participate.objects.all()
    serializer_class = ParticipateSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    def perform_create(self, serializer):
        queryset = Participate.objects.filter(user=self.request.user,gathering=serializer.validated_data.get('gathering'))
        if queryset.exists():
            raise APIException("You have signed up")
        instance = serializer.save(user=self.request.user)

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    def perform_create(self, serializer):
        # Include the owner attribute directly, rather than from request data.
        instance = serializer.save(user=self.request.user)

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter