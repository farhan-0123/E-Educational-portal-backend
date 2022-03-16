from django.http.response import HttpResponse

from rest_framework.authtoken.views import APIView
from rest_framework import status, authentication, permissions, parsers
from rest_framework.response import Response

import mimetypes

from .models import ExtendedUserProfile, Assignment, AssignmentComplete, Student, Subject, Exam, ExamQuestion, \
    ExamOption, ExamResult, StudentSubjectAttendance


class StudentProfileView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        extra_user_detail = ExtendedUserProfile.objects.get(user=request.user)
        student_details = Student.objects.get(user=request.user)

        attendance = []

        for subject in Subject.objects.filter(class_fk=student_details.class_fk):
            attendance.append({
                "name": subject.subject_name,
                "value": StudentSubjectAttendance.objects.get(student_fk=request.user, subject_fk=subject).attendance
            })

        marks_list = []

        for mark_sheet in ExamResult.objects.filter(student_fk=request.user):
            marks_list.append(
                {
                    "name": mark_sheet.date,
                    "value": mark_sheet.result
                }
            )

        marks_list.append({
            "name": "Next Week 1 Prediction",
            "Value": student_details.week_one_prediction
        })

        marks_list.append({
            "name": "Next Week 2 Prediction",
            "Value": student_details.week_two_prediction
        })

        user_details = {
            "UserName": request.user.username,
            "image": extra_user_detail.image_link,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "date_of_birth": extra_user_detail.date_of_birth,
            "gender": extra_user_detail.get_gender_display(),
            "designation": extra_user_detail.get_designation_display(),
            "Semester": student_details.class_fk.semester,
            "course": student_details.course,
            "s_mobile": extra_user_detail.phone,
            "p_mobile": student_details.parent_phone,
            "branch_name": student_details.class_fk.branch_fk.branch_name,
            "branch_code": student_details.class_fk.branch_fk.branch_code,
            "present_days": student_details.present_days,
            "free_status": student_details.fee_status,
            "backlog_count": student_details.backlog_count,
            "attendance": attendance,
            "marks": marks_list
        }

        return Response(user_details)


class StudentSubjectView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        class_fk = Student.objects.get(user=request.user).class_fk
        subject_list = Subject.objects.filter(class_fk=class_fk)

        result_list = [{
            "subject_code": subject.subject_code,
            "subject_name": subject.subject_name,
            "subject_credits": subject.subject_credits,
            "subject_photo": subject.subject_photo_url,
            "link": "https://s3-ap-southeast-1.amazonaws.com/gtusitecirculars/Syallbus/"
                    + str(subject.subject_code)
                    + ".pdf",
        } for subject in subject_list]

        return Response(result_list)


class StudentAssignmentListView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        _BASE_URL_PATH = str(request.build_absolute_uri()).replace("studentassignmentlist/", "assignmentfiledownload/")

        student = Student.objects.get(user=request.user)
        subject = Subject.objects.get(class_fk=student.class_fk, subject_code=int(request.data["subject_code"]))
        assignment_list = Assignment.objects.filter(subject_fk=subject)

        return_data = []
        for assignment in assignment_list:
            file_path = assignment.assignment_file.name
            file_name = file_path.split("/")[-1]
            assignment_complete_queryset = AssignmentComplete.objects.filter(assignment_fk=assignment,
                                                                             student_fk=request.user)
            if len(assignment_complete_queryset) == 1:
                assignment_file_path = assignment_complete_queryset[0].assignment_file.name
                assignment_file_name = assignment_file_path.split("/")[-1]

                return_data.append(
                    {
                        "link": _BASE_URL_PATH + str(assignment.assignment_pk),
                        "file_id": assignment.assignment_pk,
                        "file_name": file_name,
                        "date_created": assignment.assignment_date,
                        "submitted_file": assignment_file_name,
                        "submitted_file_id": assignment_complete_queryset[0].assignment_complete_pk
                    }
                )
            else:
                return_data.append(
                    {
                        "link": _BASE_URL_PATH + str(assignment.assignment_pk),
                        "file_id": assignment.assignment_pk,
                        "file_name": file_name,
                        "date_created": assignment.assignment_date,
                        "submitted_file": "",
                        "submitted_file_id": "",
                    }
                )

        return Response(return_data)


class StudentSubjectStudentView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        student = Student.objects.get(user=request.user)
        student_list = Student.objects.filter(class_fk=student.class_fk)

        return_list = [
            {
                "student_id": student.user.id,
                "student_first_name": student.user.first_name,
                "student_last_name": student.user.last_name,
                "student_email": student.user.email,
            } for student in student_list
        ]

        return Response(return_list)


class StudentExamView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        exam = Exam.objects.all()[0]

        question_queryset = ExamQuestion.objects.filter(exam_fk=exam)
        question_option = ExamOption.objects.all()
        return_list = []

        for question in question_queryset:
            option_queryset = question_option.filter(exam_question_fk=question)
            answer = ["A", "B", "C", "D"]
            count = 0

            for option in option_queryset:
                if option.is_this_answer:
                    break
                count += 1

            return_list.append(
                {
                    "question": question.question,
                    "optionA": option_queryset[0].option_text,
                    "optionB": option_queryset[1].option_text,
                    "optionC": option_queryset[2].option_text,
                    "optionD": option_queryset[3].option_text,
                    "correctAns": answer[count]
                }
            )

        return Response(return_list)


ANSWER_OPTION = ['A', 'B', 'C', 'D']


class StudentTestCheckView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        exam = Exam.objects.all()[0]

        if ExamResult.objects.filter(date=exam.exam_date, student_fk=request.user).count() == 1:
            result_obj = ExamResult.objects.get(date=exam.exam_date, student_fk=request.user)

            if result_obj.exam_complete:
                return Response("Exam Already Taken")

            if request.data.__contains__("StartExam"):
                question = ExamQuestion.objects.get(id=result_obj.previous_question_id)
                option_queryset = ExamOption.objects.filter(exam_question_fk=question)

                return_data = {
                    "question_id": question.id,
                    "question": question.question,
                    "optionA": option_queryset[0].option_text,
                    "optionB": option_queryset[1].option_text,
                    "optionC": option_queryset[2].option_text,
                    "optionD": option_queryset[3].option_text,
                    "result": result_obj.result,
                }

                return Response(return_data)

            if request.data.__contains__("question_id"):
                question_list = ExamQuestion.objects.all()
                current_question = question_list.get(id=request.data["question_id"])

                if current_question.id < result_obj.previous_question_id:
                    return Response("Question Already Answered")

                option_queryset = ExamOption.objects.filter(exam_question_fk=current_question)

                if option_queryset[ANSWER_OPTION.index(request.data["answer"])].is_this_answer:
                    result_obj.result += 1
                    result_obj.save()

                encounter = False

                for question in question_list:
                    if encounter:
                        result_obj.previous_question_id = question.id
                        result_obj.save()
                        return Response(result_obj.result)

                    if question.id == request.data["question_id"]:
                        encounter = True

                result_obj = ExamResult.objects.get(date=exam.exam_date, student_fk=request.user)
                result_obj.exam_complete = True
                result_obj.save()

                return Response({"result": result_obj.result})

        if request.data.__contains__("StartExam"):
            question = ExamQuestion.objects.all()[0]
            option_queryset = ExamOption.objects.filter(exam_question_fk=question)
            ExamResult(student_fk=request.user, exam_complete=False, previous_question_id=question.id, result=0,
                       date=Exam.objects.all()[0].exam_date).save()

            return_data = {
                "question_id": question.id,
                "question": question.question,
                "optionA": option_queryset[0].option_text,
                "optionB": option_queryset[1].option_text,
                "optionC": option_queryset[2].option_text,
                "optionD": option_queryset[3].option_text,
                "result": 0,
            }

            return Response(return_data)


class StudentResultSaveView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        exam = Exam.objects.all()[0]

        has_student_already_given_exam = ExamResult.objects.filter(
            student_fk=request.user,
            date=exam.exam_date
        ).count()

        if has_student_already_given_exam == 0:
            ExamResult(student_fk=request.user, result=request.data["result"]).save()
            return Response(status=status.HTTP_200_OK)

        elif has_student_already_given_exam == 1:
            return Response("Already Given Exam")

        else:
            return Response("Something's wrong")


class StudentAssignmentDeleteView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        assignment_complete = AssignmentComplete.objects.get(
            assignment_complete_pk=request.data["id"],
            student_fk=request.user
        )
        assignment_complete.delete()

        return Response(status=status.HTTP_200_OK)


class StudentAssignmentFileUploadView(APIView):
    parser_classes = [parsers.FileUploadParser]
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        student = Student.objects.get(user=request.user)
        assignment = Assignment.objects.get(assignment_pk=request.META["HTTP_ASSIGNMENT_CODE"])
        assignment_submitted_queryset = AssignmentComplete.objects.filter(assignment_fk=assignment,
                                                                          student_fk=student.user)

        if len(assignment_submitted_queryset) == 0:
            assignmentcomplete = AssignmentComplete(
                assignment_fk=assignment,
                student_fk=student.user,
                complete=True,
                assignment_file=request.FILES["file"]
            )
            assignmentcomplete.save()

            return Response(status=status.HTTP_200_OK)
        else:
            return Response("Already Submitted")


# Todo : Deprecated
class StudentAssignmentsView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        assignments = [
            {
                "assignment_id": assignment.assignment_fk.assignment_pk,
                "assignment_title": assignment.assignment_fk.assignment_title,
                "due_date": assignment.assignment_fk.due_date,
                "complete": assignment.complete,
                "marks": assignment.marks,
            } for assignment in AssignmentComplete.objects.filter(student_fk=request.user)]

        return Response(assignments)


# Todo : Deprecated
class StudentAssignmentFileView(APIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        assignment_file_path = str(Assignment.objects.get(assignment_pk=request.data["assignment_id"]).assignment_file)
        with open(assignment_file_path, "rb") as assignment_file:
            return HttpResponse(assignment_file, content_type=mimetypes.guess_type(assignment_file_path)[0])
