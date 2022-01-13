from django.contrib.auth.models import User
from rest_framework import viewsets

from .serializers import UserSerializer


# This is not final this is only temporary
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
