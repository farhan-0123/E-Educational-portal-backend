import mimetypes

from django.http.response import HttpResponse, HttpResponseBadRequest

from rest_framework import authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import ExtendedUserProfile, Assignment, Chat, Subject, Student, Teacher, TeacherSubject


# Todo : Deprecated
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


class ChatView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            extra = ExtendedUserProfile.objects.get(user=user)
            if extra.designation == "S":
                student = Student.objects.get(user=user)
                class_ = student.class_fk
            elif extra.designation == "T":
                teacher = Teacher.objects.get(user=user)
                teacher_subject_obj_list = TeacherSubject.objects.filter(teacher_fk=teacher)
                class_ = None
                for teacher_subject_obj in teacher_subject_obj_list:
                    if teacher_subject_obj.subject_fk.subject_code == int(request.data["subject_code"]):
                        class_ = teacher_subject_obj.subject_fk.class_fk
                        break

            subject = Subject.objects.get(subject_code=request.data["subject_code"], class_fk=class_)

            if request.data.__contains__("chat"):
                chat = Chat(subject_fk=subject, user_fk=user, chat_text=request.data["chat"])
                chat.save()

            chat_list = Chat.objects.filter(subject_fk=subject)

            return_data = [
                {
                    "username": chat.user_fk.username,
                    "chat": chat.chat_text
                } for chat in chat_list
            ]

            return Response(return_data)
        except KeyError:
            return HttpResponseBadRequest("Bad Request")


@api_view()
@permission_classes([permissions.AllowAny, ])
def assignment_file_download_view(request, assignment_id):
    assignment = Assignment.objects.get(assignment_pk=assignment_id)
    type_ = mimetypes.guess_type(assignment.assignment_file.name)

    return HttpResponse(assignment.assignment_file.open(), content_type=type_[0])
