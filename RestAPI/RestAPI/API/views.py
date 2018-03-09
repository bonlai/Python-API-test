from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *

from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from rest_framework import generics
#from django_filters.rest_framework import DjangoFilterBackend
#from rest_framework import filters
from django_filters import rest_framework as filters

from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
#from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from rest_framework import mixins
from rest_framework import status
from django.db.models import Count

class ListUser(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,SearchFilter)
    filter_fields = ('id',)
    search_fields = ('username',)
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
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 3
    def get_paginated_response(self, data):
        return Response(data)
    
class GatheringFilter(filters.FilterSet):
    start_date = filters.DateTimeFilter(name="start_datetime", lookup_expr='gte')
    end_date = filters.DateTimeFilter(name="start_datetime", lookup_expr='lte')
    count_greater = filters.NumberFilter(name="member_count", lookup_expr='gte')
    count_less = filters.NumberFilter(name="member_count", lookup_expr='lte')
    location = filters.CharFilter(name="restaurant__address",lookup_expr='icontains')

    class Meta:
        model = Gathering
        fields = ['location','start_date']

class GatheringViewSet(viewsets.ModelViewSet):
    #queryset = Gathering.objects.annotate(member_count=Count('member')).all()
    serializer_class = GatheringSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,SearchFilter,OrderingFilter)
    ordering_fields = ('recommended_rate',)
    filter_class = GatheringFilter
    search_fields = ('name','details')
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    def get_queryset(self):
        for gathering in Gathering.objects.all():
            requestRestaurant=gathering.restaurant
            requestUser=self.request.user
            if not RecommendedRate.objects.filter(gathering=gathering,restaurant=requestRestaurant,
                                                  user=requestUser).exists():
                s=SlopeOne()
                value=s.predict(requestUser.id,requestRestaurant.id)     
                c=RecommendedRate(gathering=gathering,restaurant=requestRestaurant,user=requestUser,rating=value)
                c.save()

        requestUser=self.request.user
        rr=requestUser.recommendedrate_set.all().order_by('-rating')
        mkey=list(rr.values_list('gathering_id',flat=True))
        clauses = ' '.join(['WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(mkey)])
        ordering = 'CASE %s END' % clauses
        queryset = Gathering.objects.filter(pk__in=mkey).extra(
                   select={'ordering': ordering}, order_by=('ordering',))
        return queryset

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
    pagination_class = LargeResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,SearchFilter, OrderingFilter)
    filter_fields = ('average_rate',)
    ordering_fields = ('average_rate', 'review_count')
    search_fields = ('address','category','name',)

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

class UserInterestList(generics.ListAPIView):
    model = Interest
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer

    def get_queryset(self):
        id = self.kwargs['userid']
        return Interest.objects.filter(user__id=id)#user__id=id,      
    
    def delete(self, request, *args, **kwargs):
        userId=self.kwargs['userid']
        user=User.objects.get(id=userId)
        user.enjoy.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)

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