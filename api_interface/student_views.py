from django.http.response import HttpResponse

from rest_framework.authtoken.views import APIView
from rest_framework import status, authentication, permissions
from rest_framework.response import Response

import mimetypes

from .models import ExtendedUserProfile, Assignment, AssignmentComplete, Student, Class, \
    Subject, Branch, Exam, ExamQuestion, ExamOption, ExamResult


class StudentProfileView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        extra_user_detail = ExtendedUserProfile.objects.get(user=request.user)
        student_details = Student.objects.get(user=request.user)

        user_details = {
            "UserName": request.user.username,
            "image": extra_user_detail.image_link,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "date_of_birth": extra_user_detail.date_of_birth,
            "gender": extra_user_detail.get_gender_display(),
            "designation": extra_user_detail.get_designation_display(),
            "Semester": student_details.class_fk.semester,
            "course": student_details.course,
            "s_mobile": extra_user_detail.phone,
            "p_mobile": student_details.parent_phone,
            "branch_name": student_details.class_fk.branch_fk.branch_name,
            "branch_code": student_details.class_fk.branch_fk.branch_code,
            "present_days": student_details.present_days,
            "free_status": student_details.fee_status,
            "backlog_count": student_details.backlog_count
        }

        return Response(user_details)


class StudentSubjectView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        class_fk = Student.objects.get(user=request.user).class_fk
        subject_list = Subject.objects.filter(class_fk=class_fk)

        result_list = [{
            "subject_code": subject.subject_code,
            "subject_name": subject.subject_name,
            "subject_credits": subject.subject_credits,
            "subject_photo": subject.subject_photo_url,
            "link": "https://s3-ap-southeast-1.amazonaws.com/gtusitecirculars/Syallbus/"
                    + str(subject.subject_code)
                    + ".pdf",
        } for subject in subject_list]

        return Response(result_list)


class StudentAssignmentListView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        _BASE_URL_PATH = str(request.build_absolute_uri()).replace("studentassignmentlist/", "assignmentfiledownload/")

        student = Student.objects.get(user=request.user)
        subject = Subject.objects.get(class_fk=student.class_fk, subject_code=int(request.data["subject_code"]))
        assignment_list = Assignment.objects.filter(subject_fk=subject)

        return_data = []
        for assignment in assignment_list:
            file_path = assignment.assignment_file.name
            file_name = file_path.split("/")[-1]
            return_data.append(
                {
                    "link": _BASE_URL_PATH + str(assignment.assignment_pk),
                    "file_id": assignment.assignment_pk,
                    "file_name": file_name,
                    "date_created": assignment.assignment_date
                }
            )

        return Response(return_data)


class StudentSubjectStudentView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        student = Student.objects.get(user=request.user)
        student_list = Student.objects.filter(class_fk=student.class_fk)

        return_list = [
            {
                "student_id": student.user.id,
                "student_first_name": student.user.first_name,
                "student_last_name": student.user.last_name,
                "student_email": student.user.email,
            } for student in student_list
        ]

        return Response(return_list)


class StudentExamView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        exam = Exam.objects.get(exam_id="58d6eb6b-31e4-421a-a405-921c5bb6ae6f")

        question_queryset = ExamQuestion.objects.filter(exam_fk=exam)

        return_list = []

        for question in question_queryset:
            option_queryset = ExamOption.objects.filter(exam_question_fk=question)
            return_list.append(
                {
                    "question": question.question,
                    "options": [
                        {
                            "text": option.option_text,
                            "isAnswer": option.is_this_answer,
                        }
                        for option in option_queryset
                    ]
                }
            )
        return Response(return_list)


# Todo : Deprecated
class StudentAssignmentsView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        assignments = [
            {
                "assignment_id": assignment.assignment_fk.assignment_pk,
                "assignment_title": assignment.assignment_fk.assignment_title,
                "due_date": assignment.assignment_fk.due_date,
                "complete": assignment.complete,
                "marks": assignment.marks,
            } for assignment in AssignmentComplete.objects.filter(student_fk=request.user)]

        return Response(assignments)


# Todo : Deprecated
class StudentAssignmentFileView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        assignment_file_path = str(Assignment.objects.get(assignment_pk=request.data["assignment_id"]).assignment_file)
        with open(assignment_file_path, "rb") as assignment_file:
            return HttpResponse(assignment_file, content_type=mimetypes.guess_type(assignment_file_path)[0])
