from rest_framework.authtoken.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response

from .models import ExtendedUserProfile


class StudentProfileView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        extra_user_detail = ExtendedUserProfile.objects.get(user=user)

        user_details = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "date_of_birth": extra_user_detail.date_of_birth,
        }

        return Response(user_details)
