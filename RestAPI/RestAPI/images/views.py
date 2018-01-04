from images.models import Image
from images.serializers import ImagesSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImagesSerializer
    permission_classes = (IsAuthenticated,)