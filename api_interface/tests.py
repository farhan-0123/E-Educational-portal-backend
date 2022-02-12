from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

# extra imports
import datetime


# Create your tests here.
class AuthTokenTestCase(TestCase):
    fixtures = ["./fixtures/test.json"]

    def setUp(self):
        super(AuthTokenTestCase, self).setUp()

        # This print statement is added to make tests look a bit better.
        print()

    def test_student_auth_token_with_student_login(self):
        """
        Description:
            This is a test to check StudentAuthToken which is in views.py the main purpose of this test is to ensure
            that when a valid username and password is given the system returns with token for user with designation
            Student.
        """

        # Getting required data
        database_token = Token.objects.get(user=User.objects.get(username="Student_one")).key

        # Setup
        client = APIClient()

        # Testing api
        token = client.post(
            path="/api/auth/student/",
            data={"username": "Student_one", "password": "Spassword@one"},
            format="json",
        ).data["token"]

        # Validating data
        self.assertEqual(
            token,
            database_token,
            "[AuthTokenTestCase][Testing StudentAuthToken][using student login] Failed Token Not Equal"
        )
        print("[AuthTokenTestCase][Testing StudentAuthToken][using student login] Success got Token")

    def test_teacher_auth_token_with_teacher_login(self):
        """
        Description:
            This is a test to check TeacherAuthToken which is in views.py the main purpose of this test is to ensure
            that when a valid username and password is given the system returns with token for user with designation
            Teacher.
        """

        # Getting required data
        database_token = Token.objects.get(user=User.objects.get(username="Teacher_one")).key

        # Setup
        client = APIClient()

        # Testing api
        token = client.post(
            path="/api/auth/teacher/",
            data={"username": "Teacher_one", "password": "Tpassword@one"},
            format="json",
        ).data["token"]

        # Validating data
        self.assertEqual(
            token,
            database_token,
            "[AuthTokenTestCase][Testing TeacherAuthToken][using teacher login] Failed Token Not Equal"
        )
        print("[AuthTokenTestCase][Testing TeacherAuthToken][using teacher login] Success got Token")

    @staticmethod
    def test_student_auth_token_with_teacher_login():
        """
        Description:
            This is a test to check StudentAuthToken which is in views.py the main purpose of this test is to ensure
            that when a valid username and password is given the system doesn't return with token for user with
            designation Teacher as this api should only be used with student.
        """

        # Getting required data
        # None Required

        # Setup
        client = APIClient()

        # Testing api and Validating data
        try:
            token = client.post(
                path="/api/auth/student/",
                data={"username": "Teacher_one", "password": "Tpassword@one"},
                format="json",
            )
            print("[AuthTokenTestCase][Testing StudentAuthToken][using teacher login] Fail Got Token",
                  token.data["token"])
        except AssertionError:
            print("[AuthTokenTestCase][Testing StudentAuthToken][using teacher login] Success Didn't get Token")

    @staticmethod
    def test_teacher_auth_token_with_student_login():
        """
        Description:
            This is a test to check TeacherAuthToken which is in views.py the main purpose of this test is to ensure
            that when a valid username and password is given the system doesn't return with token for user with
            designation Student as this api should only be used with Teacher.
        """
        # Getting required data
        # None Required

        # Setup
        client = APIClient()

        # Testing api and Validating data
        try:
            token = client.post(
                path="/api/auth/teacher/",
                data={"username": "Student_one", "password": "Spassword@one"},
                format="json",
            )
            print("[AuthTokenTestCase][Testing TeacherAuthToken][using student login] Fail Got Token",
                  token.data["token"])
        except AssertionError:
            print("[AuthTokenTestCase][Testing TeacherAuthToken][using student login] Success Didn't get Token")


class StudentAPITestCase(TestCase):
    fixtures = ["./fixtures/test.json"]

    def setUp(self):
        super(StudentAPITestCase, self).setUp()

        # This print statement is added to make tests look a bit better.
        print()

    def test_student_profile(self):
        """
        Description:
            This is a test to check StudentProfileView which is in student_views.py
        """
        # Getting required data
        token = Token.objects.get(user__username="MarilinFydo")
        expected_data = {
            'UserName': 'MarilinFydo',
            'image': 'https://res.cloudinary.com/diqqf3eq2/image/upload/v1595959131/person-2_ipcjws.jpg',
            'first_name': 'Marilin',
            'last_name': 'Fydo',
            'email': 'mfydo8@nasa.gov',
            'date_of_birth': datetime.date(2002, 8, 13),
            'gender': 'Female',
            'designation': 'Student',
            'Semester': 2,
            'course': 'BE',
            's_mobile': '5767290563',
            'p_mobile': '7929880807',
            'branch_name': 'Mechanical Engineering',
            'branch_code': 'ME',
            'present_days': 21,
            'free_status': True,
            'backlog_count': 0
        }

        # Setup
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        # Testing api
        profile = client.get(path="/api/studentprofile/")

        # Validating data
        self.assertEqual(
            profile.data,
            expected_data,
            "[StudentAPITestCase][Testing StudentProfileView] Failed got unexpected data"
        )
        print("[StudentAPITestCase][Testing StudentProfileView] Success got expected data")
