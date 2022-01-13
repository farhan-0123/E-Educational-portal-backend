from django.contrib.auth.models import User
from .models import ExtendedUserProfile
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import UserSerializer


# This is not final this is only temporary
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        userdetail = ExtendedUserProfile.objects.get(user=user)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'designation': userdetail.designation
        })
