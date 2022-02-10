import mimetypes

from django.http.response import HttpResponse

from rest_framework import status, authentication, permissions, parsers
from rest_framework.authtoken.views import APIView
from rest_framework.response import Response

from .models import ExtendedUserProfile, Teacher, TeacherSubject, Student, Assignment


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
                "subject_photo": teacher_subject_obj.subject_fk.subject_photo_url,
                "semester": teacher_subject_obj.subject_fk.class_fk.semester,
                "branch": teacher_subject_obj.subject_fk.class_fk.branch_fk.branch_name,
                "link": "https://s3-ap-southeast-1.amazonaws.com/gtusitecirculars/Syallbus/"
                        + str(teacher_subject_obj.subject_fk.subject_code)
                        + ".pdf",
            } for teacher_subject_obj in teacher_subject_obj_list
        ]

        return Response(return_data)


class TeacherSubjectStudentView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        teacher = Teacher.objects.get(user=request.user)
        teacher_subject_obj_list = TeacherSubject.objects.filter(teacher_fk=teacher)
        class_ = None
        for teacher_subject_obj in teacher_subject_obj_list:
            if teacher_subject_obj.subject_fk.subject_code == int(request.data["subject_code"]):
                class_ = teacher_subject_obj.subject_fk.class_fk
                break
        student_list = Student.objects.filter(class_fk=class_)

        return_list = [
            {
                "student_id": student.user.id,
                "student_first_name": student.user.first_name,
                "student_last_name": student.user.last_name,
                "student_email": student.user.email,
            } for student in student_list
        ]

        return Response(return_list)


class TeacherAssignmentFileUploadView(APIView):
    parser_classes = [parsers.FileUploadParser]
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        teacher = Teacher.objects.get(user=request.user)
        teacher_subject_obj_list = TeacherSubject.objects.filter(teacher_fk=teacher)
        subject = None

        for teacher_subject_obj in teacher_subject_obj_list:
            if teacher_subject_obj.subject_fk.subject_code == int(request.META["HTTP_SUBJECT_CODE"]):
                subject = teacher_subject_obj.subject_fk
                break

        assignment = Assignment(subject_fk=subject, assignment_file=request.FILES["file"])
        assignment.save()

        return Response(status=status.HTTP_200_OK)


class TeacherAssignmentListView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        _BASE_URL_PATH = str(request.build_absolute_uri()).replace("teacherassignmentlist/", "assignmentfiledownload/")
        teacher = Teacher.objects.get(user=request.user)
        teacher_subject_obj_list = TeacherSubject.objects.filter(teacher_fk=teacher)

        subject = None
        for teacher_subject_obj in teacher_subject_obj_list:
            if teacher_subject_obj.subject_fk.subject_code == int(request.data["subject_code"]):
                subject = teacher_subject_obj.subject_fk
                break

        assignment_list = Assignment.objects.filter(subject_fk=subject)

        return_data = []
        for assignment in assignment_list:
            file_path = assignment.assignment_file.name
            file_name = file_path.split("/")[-1]
            return_data.append(
                {
                    "link": _BASE_URL_PATH + str(assignment.assignment_pk),
                    "id": assignment.assignment_pk,
                    "file_name": file_name,
                    "date_created": assignment.assignment_date
                }
            )

        return Response(return_data)


class TeacherAssignmentDeleteView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        assignment = Assignment.objects.get(assignment_pk=request.data["id"])
        assignment.delete()

        return Response(status=status.HTTP_200_OK)


# Todo : Following class is Deprecated
class TeacherAssignmentFileDownloadView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        assignment = Assignment.objects.get(assignment_pk=request.data["id"])
        type_ = mimetypes.guess_type(assignment.assignment_file.name)

        return HttpResponse(assignment.assignment_file.open(), content_type=type_[0])
