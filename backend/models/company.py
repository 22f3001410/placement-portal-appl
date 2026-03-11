from extensions import db

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    company_name = db.Column(db.String(150))
    hr_contact = db.Column(db.String(150))
    website = db.Column(db.String(150))
    approval_status = db.Column(db.String(20), default="Pending")