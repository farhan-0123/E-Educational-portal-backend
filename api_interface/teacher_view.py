from django.http.response import HttpResponse

from rest_framework.authtoken.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response

import mimetypes

from .models import ExtendedUserProfile, Assignment, AssignmentComplete, Exam, ExamResult, Teacher, Student, Class, \
    Subject, Branch


class TeacherProfileView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        extra_user_detail = ExtendedUserProfile.objects.get(user=request.user)
        teacher_details = Teacher.objects.get(user=request.user)

        user_details = {
            "UserName": request.user.username,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "date_of_birth": extra_user_detail.date_of_birth,
            "gender": extra_user_detail.get_gender_display(),
            "designation": extra_user_detail.get_designation_display(),
            "Semester": teacher_details.class_fk.semester,
            "branch_name": teacher_details.class_fk.branch_fk.branch_name,
            "branch_code": teacher_details.class_fk.branch_fk.branch_code,
        }

        return Response(user_details)
