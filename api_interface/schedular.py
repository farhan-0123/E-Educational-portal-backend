from apscheduler.schedulers.background import BackgroundScheduler
from .models import Chat, ExamQuestion
from django.utils import timezone


def chat_delete():
    from datetime import datetime
    print("SCHEDULER Deleting the chat...", datetime.now())
    Chat.objects.all().delete()


def exam_delete():
    from datetime import datetime
    print("SCHEDULER Deleting the Exam...", datetime.now())
    ExamQuestion.objects.all().delete()


def start_scheduler():
    print("Starting the background scheduler...")
    scheduler = BackgroundScheduler(timezone=timezone.get_current_timezone_name())
    scheduler.add_job(chat_delete, 'interval', days=1)
    scheduler.add_job(exam_delete, 'cron', day_of_week='mon')
    scheduler.start()
