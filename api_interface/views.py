import mimetypes

from django.http.response import HttpResponse

from rest_framework import authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import ExtendedUserProfile, Assignment


class SubjectDetailsLinkView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return Response(
            {
                "link": "https://s3-ap-southeast-1.amazonaws.com/gtusitecirculars/Syallbus/" +
                        str(request.data["subject_code"]) +
                        ".pdf"
            }
        )


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


@api_view()
@permission_classes([permissions.AllowAny, ])
def assignment_file_download_view(request, id):
    assignment = Assignment.objects.get(assignment_pk=id)
    type_ = mimetypes.guess_type(assignment.assignment_file.name)

    return HttpResponse(assignment.assignment_file.open(), content_type=type_[0])
