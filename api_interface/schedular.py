from apscheduler.schedulers.background import BackgroundScheduler
from .models import Chat, ExamQuestion, Exam, ExamResult, Student
from django.utils import timezone
from datetime import datetime, date
from numpy import array
from sklearn.linear_model import LinearRegression

scheduler = BackgroundScheduler(timezone=timezone.get_current_timezone_name())


def chat_delete():
    print("SCHEDULER Deleting the chat...", datetime.now())
    Chat.objects.all().delete()


def exam_delete():
    print("SCHEDULER Deleting the Exam...", datetime.now())
    ExamQuestion.objects.all().delete()
    exam = Exam.objects.all()[0]
    exam.exam_date = date.today()
    exam.save()


def prediction_model():
    print("SCHEDULER Predicting this weeks result...")
    results = ExamResult.objects.all()
    student_list = Student.objects.all()

    scheduler.remove_job("prediction_model")

    for student in student_list:

        student_result = results.filter(student_fk=student.user)

        if not len(student_result) == 0:
            x_date_list = []
            y_result_list = []

            for result in student_result:
                x_date_list.append(result.date.toordinal())
                y_result_list.append(result.result)

            x_numpy = array(x_date_list).reshape((-1, 1))
            x_numpy = x_numpy - x_numpy.min()
            y_numpy = array(y_result_list)

            model = LinearRegression()
            model.fit(x_numpy, y_numpy)
            print(model.predict(array([x_numpy.max() + 7, ]).reshape(-1, 1)))


def start_scheduler():
    print("Starting the background scheduler...")
    scheduler.add_job(chat_delete, 'interval', days=1)
    scheduler.add_job(exam_delete, 'cron', day_of_week='mon')
    # scheduler.add_job(prediction_model, 'interval', seconds=1, id="prediction_model")
    scheduler.start()
