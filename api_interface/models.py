import uuid, datetime

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ExtendedUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=False)
    image_link = models.URLField()
    phone = models.CharField(max_length=15, null=False, default="+99999999999999")
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
    designation = models.CharField(
        null=False,
        max_length=1,
        choices=[
            ("S", "Student"),
            ("T", "Teacher"),
            ("A", "Admin")
        ],
        default="S"
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Branch(models.Model):
    branch_pk = models.IntegerField(primary_key=True, auto_created=True, editable=False)
    branch_code = models.CharField(max_length=3)
    branch_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.branch_name}"


class Class(models.Model):
    class_pk = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch_fk = models.ForeignKey(Branch, rel=models.ManyToOneRel, on_delete=models.DO_NOTHING)
    semester = models.IntegerField(
        validators=[
            MaxValueValidator(limit_value=8, message="Semester cannot be more than 8"),
            MinValueValidator(limit_value=1, message="Semester cannot be more less 1")
        ],
    )

    def __str__(self):
        return f"Branch : {self.branch_fk.branch_name} and Semester: {self.semester}"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    class_fk = models.ForeignKey(Class, rel=models.ManyToOneRel, on_delete=models.DO_NOTHING)
    course = models.CharField(max_length=10, null=False, default="NAN")
    present_days = models.IntegerField()
    fee_status = models.BooleanField()
    backlog_count = models.IntegerField()
    parent_phone = models.CharField(max_length=15, default="+99999999999999")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Subject(models.Model):
    class_fk = models.ForeignKey(Class, rel=models.ManyToOneRel, on_delete=models.DO_NOTHING)
    subject = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject_code = models.IntegerField()
    subject_name = models.CharField(max_length=100)
    subject_credits = models.IntegerField()
    subject_photo_url = models.URLField(default="null")

    def __str__(self):
        return f" Subject Code: {self.subject_code} Subject Name: {self.subject_name}"


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING, null=True)
    field_of_knowledge = models.CharField(max_length=200)
    salary = models.IntegerField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class TeacherSubject(models.Model):
    teacher_subject_pk = models.IntegerField(primary_key=True, auto_created=True, editable=False)
    teacher_fk = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    subject_fk = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"Teacher: {self.teacher_fk} {self.subject_fk}"


def custom_file_path(instance, filename):
    return "/".join([
        "student_assignments",
        instance.subject_fk.class_fk.branch_fk.branch_name,
        str(instance.subject_fk.subject_code),
        datetime.date.today().isoformat(),
        filename
    ])


class Assignment(models.Model):
    assignment_pk = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    subject_fk = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, null=True)
    assignment_date = models.DateField(auto_now=True)
    assignment_file = models.FileField(upload_to=custom_file_path)

    def __str__(self):
        file_path = str(self.assignment_file)
        file_name = file_path.split("/")[-1]
        return f"{self.subject_fk} File Name: {file_name} Creation Date: {self.assignment_date}"

    def delete(self, using=None, keep_parents=False):
        self.assignment_file.storage.delete(self.assignment_file.name)
        super().delete()


class AssignmentComplete(models.Model):
    assignment_fk = models.ForeignKey(Assignment, rel=models.ManyToOneRel, on_delete=models.DO_NOTHING)
    student_fk = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    class_fk = models.ForeignKey(Class, rel=models.ManyToOneRel, on_delete=models.DO_NOTHING, null=True)
    complete = models.BooleanField()
    marks = models.IntegerField(
        validators=[
            MaxValueValidator(limit_value=200, message="Value more than 200"),
            MinValueValidator(limit_value=0, message="Value less than 0")
        ]
    )

    def __str__(self):
        if self.complete:
            return f"Assignment: {self.assignment_fk.assignment_title}" \
                   f" is completed by {self.student_fk.first_name} {self.student_fk.last_name}"
        else:
            return f"Assignment: {self.assignment_fk.assignment_title}" \
                   f" is not completed by {self.student_fk.first_name} {self.student_fk.last_name}"


class Exam(models.Model):
    exam = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    subject_fk = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, null=True)
    class_fk = models.ForeignKey(Class, rel=models.ManyToOneRel, on_delete=models.DO_NOTHING, null=True)
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
        return f"{self.subject_fk.subject_name} {self.exam_title} {self.exam_date}"


class ExamResult(models.Model):
    exam_fk = models.ForeignKey(Exam, on_delete=models.DO_NOTHING)
    student_fk = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    class_fk = models.ForeignKey(Class, rel=models.ManyToOneRel, on_delete=models.DO_NOTHING, null=True)
    result = models.IntegerField(
        validators=[
            MaxValueValidator(limit_value=200, message="Value more than 200"),
            MinValueValidator(limit_value=0, message="Value less than 0")
        ]
    )

    def __str__(self):
        return f"Student {self.student_fk.first_name} {self.student_fk.last_name} got {self.result}" \
               f" from Exam {self.exam_fk.exam_title} "


class Chat(models.Model):
    subject_fk = models.ForeignKey(Subject, on_delete=models.CASCADE)
    user_fk = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    chat_text = models.CharField(max_length=500)
    time_stamp = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.subject_fk} {self.time_stamp}"
