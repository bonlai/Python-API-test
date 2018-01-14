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
#router.register(r'profilePic', ProfilePicViewSet)
#router.register(r'profile', ProfileViewSet)
router.register(r'gathering', GatheringViewSet)
router.register(r'restaurantImage', RestaurantImageViewSet)
router.register(r'participate', ParticipateViewSet)
router.register(r'restaurant', RestaurantViewSet)
router.register(r'Interest', InterestViewSet)
router.register(r'review', ReviewViewSet)



urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/api/')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
    #url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api/profile/(?P<pk>[0-9]+)/$', ProfileDetail.as_view()),
    url(r'^api/profile/(?P<pk>[0-9]+)/profile_pic_udate/$', ProfilePicUpdate.as_view()),
    url(r'^api/user_list/$', ListUser.as_view()),
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login')
    #url(r'^appUser/$', AppUserViewSet.testing),
]

#for media access (e.g. images)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)