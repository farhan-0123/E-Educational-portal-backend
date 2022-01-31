from django.contrib import admin
from .models import ExtendedUserProfile, Student, Class, Teacher, Subject, Assignment, AssignmentComplete, Exam, \
    ExamResult, Branch, TeacherSubject


class ExtendedUserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'designation']
    ordering = ['user', 'gender', 'designation']
    list_filter = ['designation']


admin.site.register(ExtendedUserProfile, ExtendedUserProfileAdmin)
admin.site.register(Student)


class ClassAdmin(admin.ModelAdmin):
    list_display = ['branch_fk', 'semester']
    ordering = ['branch_fk', 'semester']


admin.site.register(Class, ClassAdmin)
admin.site.register(Teacher)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['subject_code', 'subject_name', 'branch', 'semester']
    ordering = ['subject_name', 'subject_code']
    list_filter = ['class_fk']

    def semester(self, obj):
        return obj.class_fk.semester

    def branch(self, obj):
        return obj.class_fk.branch_fk


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Assignment)
admin.site.register(AssignmentComplete)
admin.site.register(Exam)
admin.site.register(ExamResult)
admin.site.register(Branch)
admin.site.register(TeacherSubject)
