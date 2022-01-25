from django.urls import path
from django.conf.urls import include

from rest_framework import routers

from .views import UserProfileImageView, StudentAuthToken, TeacherAuthToken, AdminAuthToken
from .student_views import StudentProfileView, StudentAssignmentsView, StudentAssignmentFileView, StudentExamResultView, \
    StudentSubjectView
from .teacher_view import TeacherProfileView

router = routers.DefaultRouter()

urlpatterns = [
    # common end points
    path('', include(router.urls)),
    path('auth/student/', StudentAuthToken.as_view()),
    path('auth/teacher/', TeacherAuthToken.as_view()),
    path('auth/admin/', AdminAuthToken.as_view()),
    path('userprofileimage/', UserProfileImageView.as_view()),

    # student end points
    path('studentprofile/', StudentProfileView.as_view()),
    path('studentsubject/', StudentSubjectView.as_view()),
    path('studentassignments/', StudentAssignmentsView.as_view()),
    path('studentassignmentfile/', StudentAssignmentFileView.as_view()),
    path('studentexamresults/', StudentExamResultView.as_view()),

    # teacher end points
    path('teacherprofile/', TeacherProfileView.as_view())

]
