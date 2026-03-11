from extensions import celery, mail
from models import Application, Student, Drive, Company, User
from flask_mail import Message
import csv
import os

@celery.task(bind=True)
def export_student_applications(self, student_id):

    applications = Application.query.filter_by(student_id=student_id).all()

    filename = f"exports/student_{student_id}.csv"
    os.makedirs("exports", exist_ok=True)

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Student ID",
            "Company Name",
            "Drive Title",
            "Application Status",
            "Application Date",
            "Interview Date"
        ])

        for app in applications:
            drive = Drive.query.get(app.drive_id)
            company = Company.query.get(drive.company_id) if drive else None
            writer.writerow([
                student_id,
                company.company_name if company else "N/A",
                drive.job_title if drive else "N/A",
                app.status,
                app.application_date or "N/A",
                app.interview_date.isoformat() if app.interview_date else "Not Scheduled"
            ])

    student = Student.query.get(student_id)
    user = User.query.get(student.user_id)

    with open(filename, "r") as f:
        csv_data = f.read()

    msg = Message(
        subject="Your Application Export is Ready",
        recipients=[user.email],
        html=f"""
        <div style="font-family:Arial,sans-serif;max-width:500px;margin:auto;padding:30px;background:#f9f9f9;border-radius:10px;">
          <h2 style="color:#1a1a2e;">Export Complete ✅</h2>
          <p>Hi <b>{student.name}</b>,</p>
          <p>Your placement application history has been successfully exported.</p>
          <p style="color:#888;font-size:12px;">This is an automated message from Placement Portal.</p>
        </div>
        """
    )

    msg.attach(
        "applications.csv",
        "text/csv",
        csv_data
    )

    mail.send(msg)

    return filename