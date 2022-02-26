from django.contrib import admin
from .models import ExtendedUserProfile, Student, Class, Teacher, Subject, Assignment, AssignmentComplete, Exam, \
    ExamResult, Branch, TeacherSubject, Chat, ExamQuestion, ExamOption


class ExtendedUserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'designation']
    ordering = ['user', 'gender', 'designation']
    list_filter = ['designation']


admin.site.register(ExtendedUserProfile, ExtendedUserProfileAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_display = ["user", "parent_phone"]
    list_filter = ['class_fk__branch_fk__branch_name', 'class_fk__semester', "fee_status"]


admin.site.register(Student, StudentAdmin)


class ClassAdmin(admin.ModelAdmin):
    list_display = ['branch_fk', 'semester']
    ordering = ['branch_fk', 'semester']


admin.site.register(Class, ClassAdmin)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ["user", 'field_of_knowledge', 'salary']
    ordering = ["user", "salary"]
    list_filter = ["branch"]


admin.site.register(Teacher, TeacherAdmin)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ['subject_code', 'subject_name', 'branch', 'semester']
    list_filter = ['class_fk__branch_fk__branch_name', 'class_fk__semester']

    def semester(self, obj):
        return obj.class_fk.semester

    def branch(self, obj):
        return obj.class_fk.branch_fk


admin.site.register(Subject, SubjectAdmin)


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['subject_fk', 'assignment_date', 'assignment']
    list_filter = ['assignment_date', 'subject_fk__class_fk__branch_fk__branch_name']

    def assignment(self, obj):
        file_path = str(obj.assignment_file)
        file_name = file_path.split("/")[-1]
        return file_name


admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(AssignmentComplete)

admin.site.register(Exam)
admin.site.register(ExamQuestion)
admin.site.register(ExamOption)
admin.site.register(ExamResult)

admin.site.register(Branch)


class TeacherSubjectAdmin(admin.ModelAdmin):
    list_display = ['teacher_fk', 'code', 'subject']
    ordering = ['teacher_fk', 'subject_fk']
    list_filter = ['subject_fk__class_fk__branch_fk__branch_name', 'subject_fk__class_fk__semester']

    def code(self, obj):
        return obj.subject_fk.subject_code

    def subject(self, obj):
        return obj.subject_fk.subject_name


admin.site.register(TeacherSubject, TeacherSubjectAdmin)


class ChatAdmin(admin.ModelAdmin):
    list_display = ["subject_fk", "user_fk", "chat_text", "time_stamp"]
    list_filter = ['subject_fk__class_fk__branch_fk__branch_name', 'subject_fk__class_fk__semester', "time_stamp"]
    ordering = ["time_stamp"]


admin.site.register(Chat, ChatAdmin)
