from extensions import celery, mail
from models import Drive, Application
from flask_mail import Message
from datetime import datetime, timedelta
from flask import render_template


@celery.task
def send_monthly_report():
    today = datetime.utcnow()
    start = today.replace(day=1)
    prev_month = start - timedelta(days=1)
    start_prev = prev_month.replace(day=1)

    drives = Drive.query.filter(
        Drive.created_at >= start_prev,
        Drive.created_at < start
    ).all()

    total_drives = len(drives)
    drive_ids = [d.id for d in drives]

    applications = Application.query.filter(
        Application.drive_id.in_(drive_ids)
    ).count()

    selected = Application.query.filter(
        Application.drive_id.in_(drive_ids),
        Application.status == "Selected"
    ).count()

    html = render_template(
        "monthly_report.html",
        drives=total_drives,
        applications=applications,
        selected=selected,
        now=datetime.utcnow()
    )

    msg = Message(
        subject="Monthly Placement Activity Report",
        recipients=["mahichoudhary1328@gmail.com"],
        html=html
    )

    mail.send(msg)
    return "Monthly report sent"