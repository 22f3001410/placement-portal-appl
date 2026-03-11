from celery_worker import celery
from models import Student, Drive
from extensions import mail
from flask_mail import Message
from datetime import datetime, timedelta

@celery.task
def send_daily_reminders():

    today = datetime.utcnow()
    upcoming = today + timedelta(days=2)

    drives = Drive.query.filter(
        Drive.deadline >= today,
        Drive.deadline <= upcoming,
        Drive.status == "Approved"
    ).all()

    if not drives:
        return "No upcoming drives"

    students = Student.query.all()

    for student in students:

        body = "Upcoming application deadlines:\n\n"

        for d in drives:
            body += f"{d.job_title} - Deadline: {d.deadline}\n"

        msg = Message(
            subject="Placement Reminder",
            recipients=[student.email],
            body=body
        )

        mail.send(msg)

    return "Reminders sent"