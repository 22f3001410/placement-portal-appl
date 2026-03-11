from celery_worker import celery
from models import Student, Company, Drive, Application, User
from datetime import datetime, timedelta

from flask_mail import Message
from extensions import mail

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


# DAILY REMINDER EMAIL
@celery.task
def daily_deadline_check():

    tomorrow = datetime.utcnow() + timedelta(days=1)

    drives = Drive.query.filter(
        Drive.deadline <= tomorrow,
        Drive.status == "Approved"
    ).all()

    for drive in drives:

        applications = Application.query.filter_by(drive_id=drive.id).all()

        for app in applications:

            student = Student.query.get(app.student_id)

            if student:
                user = User.query.get(student.user_id)

                msg = Message(
                    subject="Placement Drive Deadline Reminder",
                    recipients=[user.email]
                )

                msg.body = f"""
Hello {student.name},

Reminder that the placement drive "{drive.job_title}" deadline is approaching.

Deadline: {drive.deadline}

Please log in to the placement portal to complete your application.

Placement Portal
"""

                mail.send(msg)


# MONTHLY REPORT EMAIL
@celery.task
def monthly_report():

    total_drives = Drive.query.count()
    total_students = Student.query.count()
    total_applications = Application.query.count()
    total_selected = Application.query.filter_by(status="Selected").count()

    styles = getSampleStyleSheet()

    report = [
        Paragraph("Monthly Placement Report", styles["Title"]),
        Paragraph(f"Total Drives: {total_drives}", styles["Normal"]),
        Paragraph(f"Total Students: {total_students}", styles["Normal"]),
        Paragraph(f"Total Applications: {total_applications}", styles["Normal"]),
        Paragraph(f"Total Selected: {total_selected}", styles["Normal"]),
    ]

    pdf_path = "monthly_report.pdf"
    pdf = SimpleDocTemplate(pdf_path)
    pdf.build(report)

    # send report to admin
    admin = User.query.filter_by(role="admin").first()

    if admin:

        msg = Message(
            subject="Monthly Placement Report",
            recipients=[admin.email]
        )

        msg.body = "Monthly placement report attached."

        with open(pdf_path, "rb") as f:
            msg.attach("monthly_report.pdf", "application/pdf", f.read())

        mail.send(msg)

    print("Monthly report generated and sent to admin")