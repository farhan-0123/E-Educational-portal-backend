from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import UserViewSet
from rest_framework.authtoken.views import obtain_auth_token


router = routers.DefaultRouter()
# This is not final this is only temporary
router.register('user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', obtain_auth_token)
]
