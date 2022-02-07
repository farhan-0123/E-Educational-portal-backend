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

    def test_student_subject(self):
        # Getting required data
        token = Token.objects.get(user__username="MarilinFydo")
        expected_data = [{'subject_code': 3110002, 'subject_name': 'English', 'subject_credits': 3,
                          'subject_photo': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQsK6sNyy6Ds6Q-nFnOCBVoK_IaCLJEXeyI6w&usqp=CAU'},
                         {'subject_code': 3110013, 'subject_name': 'Eng. Graphics & Design', 'subject_credits': 4,
                          'subject_photo': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSwzgcHMUMWvkR-TSpVJavBFoU99bL5XeGjng&usqp=CAU'},
                         {'subject_code': 3110012, 'subject_name': 'Workshop/Manufacturing', 'subject_credits': 2,
                          'subject_photo': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2skUx6jpFLLGKbdbB127twSnr8TroMzrMzw&usqp=CAU'},
                         {'subject_code': 3110015, 'subject_name': 'Mathematics - 2', 'subject_credits': 5,
                          'subject_photo': 'https://studiousguy.com/wp-content/uploads/2019/10/maths-applications.jpg'},
                         {'subject_code': 3110011, 'subject_name': 'Physics', 'subject_credits': 4,
                          'subject_photo': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQxAfgg3s1fGVREzJ3fttCJvFaQboftQpEu0A&usqp=CAU'},
                         {'subject_code': 3110004, 'subject_name': 'Basic Civil Engineering', 'subject_credits': 4,
                          'subject_photo': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS2HXcemtM9GZKSrsWI6BZPWYOemm13FCtV5A&usqp=CAU'}]

        # Setup
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        # Testing api
        subject_list = client.get(path="/api/studentsubject/")

        # Validating data
        self.assertEqual(
            subject_list.data,
            expected_data,
            "[StudentAPITestCase][Testing StudentSubjectView] Failed got unexpected data"
        )
        print("[StudentAPITestCase][Testing StudentSubjectView] Success got expected data")
