from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ExtendedUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=False)
    image_id = models.ImageField(upload_to="user_profile_images/")
    gender = models.CharField(
        null=False,
        max_length=1,
        choices=[
            ("M", "Male"),
            ("F", "Female"),
            ("O", "Other")
        ],
        default="M"
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Class(models.Model):
    class_id = models.IntegerField(primary_key=True)
    branch = models.CharField(
        null=False,
        max_length=3,
        choices=[
            ("COE", "Computer Engineer"),
            ("MEE", "Mechanical Engineer"),
            ("CHE", "Chemical Engineer"),
        ],
        default="COE"
    )
    semester = models.CharField(
        null=False,
        max_length=1,
        choices=[
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
            ("7", "7"),
            ("8", "8"),
        ],
        default="1"
    )

    def __str__(self):
        return f"Branch : {self.branch} and Semester: {self.semester}"


class Student(models.Model):
    user_id: User = models.OneToOneField(User, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, rel=models.ManyToOneRel, on_delete=models.CASCADE)
    present_days = models.IntegerField(max_length=1)
    fee_status = models.BooleanField()
    backlog_count = models.IntegerField(max_length=1)

    def __str__(self):
        return f"{self.user_id.first_name} {self.user_id.last_name}"
