from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from utils.decorators import role_required
from extensions import db, cache
from models import Company, Drive, Application, Student
from datetime import datetime

company_bp = Blueprint("company", __name__, url_prefix="/company")


@company_bp.route("/dashboard", methods=["GET"])
@role_required("company")
def dashboard():
    user_id = int(get_jwt_identity())
    company = Company.query.filter_by(user_id=user_id).first()

    drives = Drive.query.filter_by(company_id=company.id).all()

    return jsonify({
        "company": company.company_name,
        "drives": [
            {
                "id": d.id,
                "title": d.job_title,
                "status": d.status,
                "applicants": Application.query.filter_by(drive_id=d.id).count()
            }
            for d in drives
        ]
    })


@company_bp.route("/create-drive", methods=["POST"])
@role_required("company")
def create_drive():
    data = request.get_json()
    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"message": "Company not found"}), 404

    if company.approval_status != "Approved":
        return jsonify({"message": "Company not approved by admin"}), 403

    deadline = datetime.strptime(data["deadline"], "%Y-%m-%d")

    if deadline < datetime.utcnow():
        return jsonify({"message": "Deadline cannot be in the past"}), 400
    
    drive = Drive(
        company_id=company.id,
        job_title=data["job_title"],
        job_description=data["job_description"],
        eligible_branch = data.get("eligible_branch"),
        min_cgpa=data["min_cgpa"],
        eligible_year=data.get("eligible_year"),
        ctc=data["ctc"],
        deadline=deadline
    )

    db.session.add(drive)
    db.session.commit()

    cache.clear()
    return jsonify({"message": "Drive created. Awaiting admin approval."})


@company_bp.route("/applications")
@role_required("company")
def view_applications():

    user_id = int(get_jwt_identity())
    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"message": "Company not found"}), 404

    drives = Drive.query.filter_by(company_id=company.id).all()

    result = []

    for drive in drives:

        apps = Application.query.filter_by(drive_id=drive.id).all()

        for a in apps:

            student = Student.query.get(a.student_id)

            result.append({
                "id": a.id,
                "student": student.name if student else "Unknown",
                "drive": drive.job_title,
                "drive_id": drive.id,
                "status": a.status,
                "interview_date": a.interview_date.strftime("%Y-%m-%dT%H:%M") if a.interview_date else "",  # ✅ format correctly
                "resume": student.resume if student else None
            })

    return jsonify(result)


@company_bp.route("/application/<int:id>/update", methods=["PUT"])
@role_required("company")
def update_application(id):
    data = request.get_json()
    application = Application.query.get(id)

    if not application:
        return jsonify({"message": "Application not found"}), 404

    application.status = data["status"]
    db.session.commit()

    cache.clear()
    return jsonify({"message": "Application updated"})

@company_bp.route("/drive/<int:drive_id>/applications")
@role_required("company")
def view_drive_applications(drive_id):

    user_id = int(get_jwt_identity())
    company = Company.query.filter_by(user_id=user_id).first()

    drive = Drive.query.filter_by(id=drive_id, company_id=company.id).first()

    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    applications = Application.query.filter_by(drive_id=drive.id).all()

    result = []

    for a in applications:
        student = Student.query.get(a.student_id)

        result.append({
            "id": a.id,
            "student": student.name if student else "Unknown",
            "status": a.status
        })

    return jsonify(result)

@company_bp.route("/application/<int:id>/schedule", methods=["PUT"])
@role_required("company")
def schedule_interview(id):

    data = request.get_json()

    application = Application.query.get(id)

    if not application:
        return jsonify({"message": "Application not found"}), 404

    interview_date = data.get("interview_date")

    if not interview_date:
        return jsonify({"message": "Interview date required"}), 400

    try:
        application.interview_date = datetime.strptime(interview_date, "%Y-%m-%dT%H:%M")
    except Exception:
        return jsonify({"message": "Invalid date format"}), 400

    application.status = "Interview Scheduled"

    db.session.commit()

    cache.clear()

    return jsonify({"message": "Interview scheduled"})

from flask import send_from_directory

from flask import send_from_directory

@company_bp.route("/resume/<filename>")
def download_resume(filename):
    return send_from_directory(
        "uploads/resumes",
        filename,
        as_attachment=False
    )