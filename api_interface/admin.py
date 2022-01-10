from django.contrib import admin
from .models import ExtendedUserProfile, Student, Class

admin.site.register(ExtendedUserProfile)
admin.site.register(Student)
admin.site.register(Class)
