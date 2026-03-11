from extensions import db
from datetime import datetime

class Drive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    job_title = db.Column(db.String(150))
    job_description = db.Column(db.Text)
    eligible_branch = db.Column(db.String(100))
    min_cgpa = db.Column(db.Float)
    eligible_year = db.Column(db.String(20))
    ctc = db.Column(db.String(100))
    deadline = db.Column(db.DateTime)
    status = db.Column(db.String(20), default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)