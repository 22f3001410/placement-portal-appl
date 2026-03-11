from celery.schedules import crontab
from config import Config
from extensions import celery


def make_celery(app):
    celery.conf.update(
        broker_url=Config.CELERY_BROKER_URL,
        result_backend=Config.CELERY_RESULT_BACKEND,
        timezone="UTC",
        task_always_eager=False,
        task_track_started=True,        # ✅
        result_expires=3600,            # ✅
        worker_prefetch_multiplier=1,   # ✅
        include=[
            "tasks.export_tasks",
            "tasks.report_tasks",
            "tasks.scheduled_tasks",
            "tasks.reminder_tasks"
        ],
        beat_schedule={
            "daily-deadline-check": {
                "task": "tasks.scheduled_tasks.daily_deadline_check",
                "schedule": 86400
            },
            "monthly-placement-report": {
                "task": "tasks.report_tasks.send_monthly_report",
                "schedule": crontab(day_of_month=1, hour=9, minute=0)
            },
            "daily-reminder-job": {
                "task": "tasks.reminder_tasks.send_daily_reminders",
                "schedule": crontab(hour=9, minute=0)
            }
        }
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery