from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid


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
    class_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    user_id: User = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    class_id = models.ForeignKey(Class, rel=models.ManyToOneRel, on_delete=models.DO_NOTHING)
    present_days = models.IntegerField()
    fee_status = models.BooleanField()
    backlog_count = models.IntegerField()

    def __str__(self):
        return f"{self.user_id.first_name} {self.user_id.last_name}"


class Subject(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.DO_NOTHING)
    subject_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.subject_name}"


class Teacher(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, rel=models.ManyToManyRel, on_delete=models.DO_NOTHING)
    subject_id = models.ForeignKey(Subject, rel=models.ManyToManyRel, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f"{self.user_id.first_name} {self.user_id.last_name}"


class Assignment(models.Model):
    assignment_id = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    subject_id = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    assignment_title = models.CharField(max_length=150)
    max_marks = models.IntegerField(
        validators=[
            MaxValueValidator(limit_value=200, message="Value more than 200"),
            MinValueValidator(limit_value=0, message="Value less than zero")
        ]
    )
    due_date = models.DateField()
    assignment_file = models.FileField(upload_to="student_assignments/")

    def __str__(self):
        return f"{self.assignment_title}"


class AssignmentComplete(models.Model):
    assignment_id: Assignment = models.ForeignKey(Assignment, rel=models.ManyToOneRel, on_delete=models.DO_NOTHING)
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    complete = models.BooleanField()
    marks = models.IntegerField(
        validators=[
            MaxValueValidator(limit_value=200, message="Value more than 200"),
            MinValueValidator(limit_value=0, message="Value less than 0")
        ]
    )

    def __str__(self):
        if self.complete:
            return f"Assignment: {self.assignment_id.assignment_title}" \
                   f" is completed by {self.student_id.first_name} {self.student_id.last_name}"
        else:
            return f"Assignment: {self.assignment_id.assignment_title}" \
                   f" is not completed by {self.student_id.first_name} {self.student_id.last_name}"


class Exam(models.Model):
    exam_id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    subject_id = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    exam_title = models.CharField(max_length=150)
    max_marks = models.IntegerField(
        validators=[
            MaxValueValidator(limit_value=200, message="Value more than 200"),
            MinValueValidator(limit_value=0, message="Value less than zero")
        ]
    )
    exam_date = models.DateField()
    exam_file = models.FileField(upload_to="student_exams/")

    def __str__(self):
        return f"{self.subject_id.subject_name} {self.exam_title} {self.exam_date}"


class ExamResult(models.Model):
    exam_id = models.ForeignKey(Exam, on_delete=models.DO_NOTHING)
    student_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    result = models.IntegerField(
        validators=[
            MaxValueValidator(limit_value=200, message="Value more than 200"),
            MinValueValidator(limit_value=0, message="Value less than 0")
        ]
    )

    def __str__(self):
        return f"Student {self.student_id.first_name} {self.student_id.last_name} got {self.result}" \
               f" from Exam {self.exam_id.exam_title} "
