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
            "image": extra_user_detail.image_link,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "joining_date": request.user.date_joined.date(),
            "date_of_birth": extra_user_detail.date_of_birth,
            "gender": extra_user_detail.get_gender_display(),
            "designation": extra_user_detail.get_designation_display(),
            "t_mobile": extra_user_detail.phone,
            "branch_name": teacher_details.class_fk.branch_fk.branch_name,
            "branch_code": teacher_details.class_fk.branch_fk.branch_code,
            "field_of_knowledge": teacher_details.field_of_knowledge,
            "salary": teacher_details.salary
        }

        return Response(user_details)
