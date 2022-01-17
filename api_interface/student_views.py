from rest_framework.authtoken.views import APIView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from .models import ExtendedUserProfile, AssignmentComplete


class StudentProfileView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        extra_user_detail = ExtendedUserProfile.objects.get(user=request.user)

        user_details = {
            "username": request.user.username,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "date_of_birth": extra_user_detail.date_of_birth,
            "gender": extra_user_detail.get_gender_display(),
            "designation": extra_user_detail.get_designation_display(),
        }

        return Response(user_details)


class StudentAssignmentsView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        assignments = [
            {
                "assignment_id": assignment.assignment_id.assignment_id,
                "assignment_title": assignment.assignment_id.assignment_title,
                "due_date": assignment.assignment_id.due_date,
                "complete": assignment.complete,
                "marks": assignment.marks,
            } for assignment in AssignmentComplete.objects.all().filter(student_id=request.user)]

        return Response(assignments)
