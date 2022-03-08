from django.urls import path
from django.conf.urls import include

from rest_framework import routers

from .views import \
    StudentAuthToken, \
    TeacherAuthToken, \
    AdminAuthToken, \
    SubjectDetailsLinkView, \
    assignment_file_download_view, \
    ChatView, \
    student_assignment_file_download_view

from .student_views import \
    StudentProfileView, \
    StudentAssignmentsView, \
    StudentAssignmentFileView, \
    StudentSubjectView, \
    StudentSubjectStudentView, \
    StudentAssignmentListView, \
    StudentExamView, \
    StudentResultSaveView, \
    StudentTestCheckView, \
    StudentAssignmentFileUploadView

from .teacher_view import \
    TeacherProfileView, \
    TeacherSubjectView, \
    TeacherSubjectStudentView, \
    TeacherAssignmentFileUploadView, \
    TeacherAssignmentListView, \
    TeacherAssignmentDeleteView, \
    TeacherAssignmentFileDownloadView, \
    TeacherExamView, \
    TeacherStudentAssignmentView

from .schedular import start_scheduler

router = routers.DefaultRouter()

urlpatterns = [
    # common end points
    path('', include(router.urls)),
    path('auth/student/', StudentAuthToken.as_view()),
    path('auth/teacher/', TeacherAuthToken.as_view()),
    path('auth/admin/', AdminAuthToken.as_view()),
    path('assignmentfiledownload/<uuid:assignment_id>', assignment_file_download_view),
    path('studentassignmentfiledownload/<uuid:assignment_id>', student_assignment_file_download_view),
    path('chat/', ChatView.as_view()),
    # Todo : Deprecated
    path('subjectdetailslink/', SubjectDetailsLinkView.as_view()),
    # End Deprecated

    # student end points
    path('studentprofile/', StudentProfileView.as_view()),
    path('studentsubject/', StudentSubjectView.as_view()),
    path('studentsubjectstudent/', StudentSubjectStudentView.as_view()),
    path('studentassignmentlist/', StudentAssignmentListView.as_view()),
    path('studentexam/', StudentExamView.as_view()),
    path('savestudentresult/', StudentResultSaveView.as_view()),
    path('studenttestcheck/', StudentTestCheckView.as_view()),
    # Todo : Deprecated
    path('studentassignments/', StudentAssignmentsView.as_view()),
    path('studentassignmentfile/', StudentAssignmentFileView.as_view()),
    path('studentassignmentfileupload/', StudentAssignmentFileUploadView.as_view()),
    # End Deprecated

    # teacher end points
    path('teacherprofile/', TeacherProfileView.as_view()),
    path('teachersubject/', TeacherSubjectView.as_view()),
    path('teachersubjectstudentlist/', TeacherSubjectStudentView.as_view()),
    path('teacherassignmentfileupload/', TeacherAssignmentFileUploadView.as_view()),
    # Note : if you want to change the url teacherassignmentlist/ you will also have to change TeacherAssignmentListView
    # as it uses this path as hard coded string.
    path('teacherassignmentlist/', TeacherAssignmentListView.as_view()),
    path('teacherassignmentdelete/', TeacherAssignmentDeleteView.as_view()),
    path('teacherexam/', TeacherExamView.as_view()),
    path('teacherstudentassignment/', TeacherStudentAssignmentView.as_view()),
    # Todo: Deprecated
    path('teacherassignmentfiledownload/', TeacherAssignmentFileDownloadView.as_view()),

]

start_scheduler()
