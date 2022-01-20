from django.http.response import HttpResponse

from rest_framework.authtoken.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response

import mimetypes

from .models import ExtendedUserProfile, Assignment, AssignmentComplete, Exam, ExamResult, Teacher, Student, Class, \
    Subject, Branch


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
            } for assignment in AssignmentComplete.objects.all().filter(student_fk=request.user)]

        return Response(assignments)


class StudentAssignmentFileView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        assignment_file_path = str(Assignment.objects.get(assignment_pk=request.data["assignment_id"]).assignment_file)
        with open(assignment_file_path, "rb") as assignment_file:
            return HttpResponse(assignment_file, content_type=mimetypes.guess_type(assignment_file_path)[0])


class StudentExamResultView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        branch_id = Branch.objects.get(branch_name=request.data["branch_name"])
        print(branch_id)
        class_id = Class.objects.filter(semester=request.data["semester"]).filter(branch_fk=branch_id)
        print(class_id[0])
        all_results = ExamResult.objects.filter(student_fk=request.user)
        print(all_results)
        all_results = ExamResult.objects.filter(class_fk=class_id[0])
        print(all_results)
        exam_results = [
            {
                "subject_name": result.exam_fk.subject_fk.subject_name,
                "exam_title": result.exam_fk.exam_title,
                "exam_date": result.exam_fk.exam_date,
                "max_marks": result.exam_fk.max_marks,
                "marks": result.result,
            } for result in all_results]

        return Response(exam_results)
