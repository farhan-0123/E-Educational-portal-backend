from django.http.response import HttpResponse

from rest_framework import authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import ExtendedUserProfile


class StudentAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_detail = ExtendedUserProfile.objects.get(user=user)

        token, created = Token.objects.get_or_create(user=user)
        if user_detail.get_designation_display() == "Student":
            return Response({
                'token': token.key,
                'designation': user_detail.get_designation_display()
            })
        else:
            return Response({
                "invalid": "You are not authorized to login here"
            })


class TeacherAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_detail = ExtendedUserProfile.objects.get(user=user)

        token, created = Token.objects.get_or_create(user=user)
        if user_detail.get_designation_display() == "Teacher":
            return Response({
                'token': token.key,
                'designation': user_detail.get_designation_display()
            })
        else:
            return Response({
                "invalid": "You are not authorized to login here"
            })


class AdminAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_detail = ExtendedUserProfile.objects.get(user=user)

        token, created = Token.objects.get_or_create(user=user)
        if user_detail.get_designation_display() == "Admin":
            return Response({
                'token': token.key,
                'designation': user_detail.get_designation_display()
            })
        else:
            return Response({
                "invalid": "You are not authorized to login here"
            })


class UserProfileImageView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_image_path = str(ExtendedUserProfile.objects.get(user=request.user).image)

        with open(user_image_path, "rb") as user_image:
            return HttpResponse(user_image, content_type="image/*")
