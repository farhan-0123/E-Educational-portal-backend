from django.urls import path
from django.conf.urls import include

from rest_framework import routers

from .views import CustomAuthToken, UserProfileImageView
from .student_views import StudentProfileView

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', CustomAuthToken.as_view()),
    path('studentprofile/', StudentProfileView.as_view()),
    path('userprofileimage/', UserProfileImageView.as_view())
]
