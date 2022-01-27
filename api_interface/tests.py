from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


# Create your tests here.
class AuthTokenTestCase(TestCase):
    fixtures = ["./fixtures/db_800.json"]

    def test_nothing(self):
        pass

    def test_student_auth_token_with_student_login(self):
        # testing random student login
        factory = APIClient()
        token = factory.post(
            path="/api/auth/student/",
            data={"username": "Student_one", "password": "Spassword@one"},
            format="json",
        ).data["token"]
        database_token = Token.objects.get(user=User.objects.get(username="Student_one")).key
        self.assertEqual(
            token,
            database_token,
            "[Testing StudentAuthToken][using student login] Failed Token Not Equal"
        )
        print("[Testing StudentAuthToken][using student login] Success got Token")

    def test_teacher_auth_token_with_teacher_login(self):
        # testing random student login
        factory = APIClient()
        token = factory.post(
            path="/api/auth/teacher/",
            data={"username": "Teacher_one", "password": "Tpassword@one"},
            format="json",
        ).data["token"]
        database_token = Token.objects.get(user=User.objects.get(username="Teacher_one")).key
        self.assertEqual(
            token,
            database_token,
            "[Testing TeacherAuthToken][using teacher login] Failed Token Not Equal"
        )
        print("[Testing TeacherAuthToken][using teacher login] Success got Token")

    def test_student_auth_token_with_teacher_login(self):
        # testing random teacher login
        factory = APIClient()
        try:
            token = factory.post(
                path="/api/auth/student/",
                data={"username": "Teacher_one", "password": "Tpassword@one"},
                format="json",
            )
            print("[Testing StudentAuthToken][using teacher login] Fail Got Token", token.data["token"])
        except AssertionError:
            print("[Testing StudentAuthToken][using teacher login] Success Didn't get Token")

    def test_teacher_auth_token_with_student_login(self):
        # testing random teacher login
        factory = APIClient()
        try:
            token = factory.post(
                path="/api/auth/teacher/",
                data={"username": "Student_one", "password": "Spassword@one"},
                format="json",
            )
            print("[Testing TeacherAuthToken][using student login] Fail Got Token", token.data["token"])
        except AssertionError:
            print("[Testing TeacherAuthToken][using student login] Success Didn't get Token")
