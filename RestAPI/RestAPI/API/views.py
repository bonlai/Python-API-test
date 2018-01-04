from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Image,ProfilePic,AppUser
from .serializers import ImagesSerializer,ProfilePicSerializer,AppUserSerializer

from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImagesSerializer
    permission_classes = (IsAuthenticated,)

class ProfilePicViewSet(viewsets.ModelViewSet):
    queryset = ProfilePic.objects.all()
    serializer_class = ProfilePicSerializer
    permission_classes = (IsAuthenticated,)

class AppUserViewSet(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    permission_classes = (IsAuthenticated,)

    @list_route(methods=['get'])
    def testing(self,request):
        serializer_context = {
            'request': request,
        }
        appUser = AppUser.objects.get(pk=2)
        serializer = AppUserSerializer(appUser,context=serializer_context)
        return Response(serializer.data)
