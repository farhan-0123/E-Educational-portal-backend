from django.contrib import admin
from .models import ExtendedUserProfile, Student, Class, Teacher, Subject, Assignment, AssignmentComplete, Exam, \
    ExamResult

admin.site.register(ExtendedUserProfile)
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Assignment)
admin.site.register(AssignmentComplete)
admin.site.register(Exam)
admin.site.register(ExamResult)
