from django.contrib import admin
from .models import ExtendedUserProfile, Student, Class, Teacher, Subject

admin.site.register(ExtendedUserProfile)
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Teacher)
admin.site.register(Subject)
