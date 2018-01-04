"""
Definition of urls for RestAPI.
"""

from API.views import ImagesViewSet,ProfilePicViewSet,AppUserViewSet

from django.views.generic.base import RedirectView

from django.conf.urls import url, include

from django.conf.urls.static import static
from django.conf import settings

import django.contrib.auth.views
from django.contrib import admin
from rest_framework.routers import DefaultRouter
# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

router = DefaultRouter()
router.register(r'images', ImagesViewSet)
router.register(r'profilePic', ProfilePicViewSet)
router.register(r'appUser', AppUserViewSet)

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/api/')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
    #url(r'^appUser/$', AppUserViewSet.testing),
]

#for media access (e.g. images)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)