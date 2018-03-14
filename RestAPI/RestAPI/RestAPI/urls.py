"""
Definition of urls for RestAPI.
"""

from API.views import *

from django.views.generic.base import RedirectView

from django.conf.urls import url, include

from django.conf.urls.static import static
from django.conf import settings

import django.contrib.auth.views
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

router = DefaultRouter()
router.register(r'gathering', GatheringViewSet,'gathering')
router.register(r'restaurantImage', RestaurantImageViewSet)
router.register(r'participate', ParticipateViewSet)
router.register(r'restaurant', RestaurantViewSet)
router.register(r'interest', InterestViewSet)
router.register(r'review', ReviewViewSet)



urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/api/')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
    #user related urls
    url(r'^api/user/$', ListUser.as_view()),
    url(r'^api/user/(?P<pk>[0-9]+)/profile/$', ProfileDetail.as_view(),name = 'add'),
    url(r'^api/user/(?P<pk>[0-9]+)/profile/profile_pic_udate/$', ProfilePicUpdate.as_view()),
    url(r'^api/user/(?P<userid>[0-9]+)/gathering/$', UserGatheringList.as_view()),
    url(r'^api/user/(?P<userid>[0-9]+)/interest/$', UserInterestList.as_view()),
    url(r'^api/user/(?P<pk>[0-9]+)/lat_long/$', LatLongView.as_view()),
#    url(r'^api/gathering/location/$', GatheringLocationList.as_view()),
    #url(r'^api/user/(?P<userid>[0-9]+)/review/$', UserGatheringList.as_view()),
    #url(r'^api/user/(?P<userid>[0-9]+)/interest/$', UserGatheringList.as_view()),
    #user registration and login url
    url(r'^api/rest-auth/', include('rest_auth.urls')),
    url(r'^api/rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api/rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login')
]

#for media access (e.g. images)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)