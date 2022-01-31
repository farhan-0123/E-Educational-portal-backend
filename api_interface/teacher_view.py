from django.http.response import HttpResponse

from rest_framework.authtoken.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response

import mimetypes

from .models import ExtendedUserProfile, Teacher, TeacherSubject


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
            "branch_name": teacher_details.branch.branch_name,
            "branch_code": teacher_details.branch.branch_code,
            "field_of_knowledge": teacher_details.field_of_knowledge,
            "salary": teacher_details.salary
        }

        return Response(user_details)


class TeacherSubjectView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        teacher_obj = Teacher.objects.get(user=request.user)
        teacher_subject_obj_list = TeacherSubject.objects.filter(teacher_fk=teacher_obj)

        return_data = [
            {
                "subject_code": teacher_subject_obj.subject_fk.subject_code,
                "subject_name": teacher_subject_obj.subject_fk.subject_name,
                "subject_credits": teacher_subject_obj.subject_fk.subject_credits,
                "subject_photo": teacher_subject_obj.subject_fk.subject_photo_url
            } for teacher_subject_obj in teacher_subject_obj_list
        ]

        return Response(return_data)
