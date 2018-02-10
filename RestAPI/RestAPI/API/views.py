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
from django.db.models import Q

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
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    def perform_create(self, serializer):
        # Include the owner attribute directly, rather than from request data.
        instance = serializer.save(user=self.request.user)

    @list_route()
    def location(self, request):
        gathering = Gathering.objects.all()
        serializer = GatheringLocationSerializer(gathering, many=True)
        return Response(serializer.data)
'''
    @detail_route(methods=['get'])
    def participant(self, request, pk=None):
        members=self.get_object.
        gathering = self.get_object()
        serializer = ProfileSerializer(user=request.data.user)
        #if serializer.is_valid():
         #   return Response({'status': 'password set'})
        #else:
        return Response({'status': 'password set'})
'''
class UserGatheringList(generics.ListAPIView):
    model = Gathering
    queryset = Gathering.objects.all()
    serializer_class = GatheringSerializer

    def get_queryset(self):
        id = self.kwargs['userid']
        return Gathering.objects.filter(Q(member__id=id ) | Q(user__id=id))#user__id=id,

class ParticipateViewSet(viewsets.ModelViewSet):
    queryset = Participate.objects.all()
    serializer_class = ParticipateSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('user','gathering')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    def perform_create(self, serializer):
        queryset = Participate.objects.filter(user=self.request.user,gathering=serializer.validated_data.get('gathering'))
        if queryset.exists():
            queryset.delete()
            raise APIException("You have signed up")
        instance = serializer.save(user=self.request.user)

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('user',)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    def perform_create(self, serializer):
        try:
            interest = Interest.objects.get(name__iexact=serializer.validated_data.get('name'))
            interest.user.add(self.request.user)
            interest.save()
        except Interest.DoesNotExist:           
            instance = serializer.save()    
            instance.user.add(self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('restaurant','user')
    def perform_create(self, serializer):
        restaurant = Restaurant.objects.get(id=self.request.POST['restaurant'])
        if restaurant.review_count == 0:
            restaurant.review_count += 1
            restaurant.average_rate+=float(self.request.POST['rating'])
        else:
            restaurant.review_count += 1
            restaurant.average_rate+=(float(self.request.POST['rating'])-restaurant.average_rate)/restaurant.review_count

        restaurant.save()
        instance = serializer.save(user=self.request.user)

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter