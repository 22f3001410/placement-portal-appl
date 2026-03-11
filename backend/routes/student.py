from flask import Blueprint, jsonify, request, send_file, send_from_directory
from flask_jwt_extended import get_jwt_identity
from utils.decorators import role_required
from extensions import db, cache
from models import Student, Drive, Application, Company
from tasks.export_tasks import export_student_applications
from celery_worker import celery
from datetime import datetime

student_bp = Blueprint("student", __name__, url_prefix="/student")


@student_bp.route("/dashboard")
@role_required("student")
@cache.cached(timeout=60)
def dashboard():

    drives = Drive.query.filter_by(status="Approved").all()

    result = []

    for d in drives:

        company = Company.query.get(d.company_id)

        if not company:
            continue

        result.append({
            "id": d.id,
            "company_name": company.company_name,
            "title": d.job_title,
            "ctc": d.ctc,
            "min_cgpa": d.min_cgpa,
            "deadline": d.deadline
        })

    return jsonify(result)

@student_bp.route("/profile")
@role_required("student")
def get_profile():
    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first()
    return jsonify({
        "id": student.id,          
        "name": student.name,
        "branch": student.branch,
        "cgpa": student.cgpa,
        "year": student.year
    })

@student_bp.route("/apply/<int:drive_id>", methods=["POST"])
@role_required("student")
def apply(drive_id):

    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message": "Student profile not found"}), 404

    drive = Drive.query.get(drive_id)

    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    if drive.deadline < datetime.utcnow():
        return jsonify({"message": "Application deadline passed"}), 400

    if drive.status != "Approved":
        return jsonify({"message": "Drive not approved"}), 403

    student_branch = student.branch.strip().lower()
    eligible = drive.eligible_branch.strip().lower()

    # allow everyone
    if "all" in eligible or "any" in eligible:
        pass
    else:
        allowed_branches = [b.strip().lower() for b in eligible.split(",")]

        if student_branch not in allowed_branches:
            return jsonify({"message": "Branch not eligible"}), 403
        
    student_year = str(student.year)
    eligible_year = str(drive.eligible_year).lower()

    # any year allowed
    if eligible_year == "any":
        pass

    # final year students
    elif eligible_year == "final":
        if int(student_year) < 3:
            return jsonify({"message": "Year not eligible"}), 403

    # specific year
    else:
        if student_year != eligible_year:
            return jsonify({"message": "Year not eligible"}), 403

    if student.cgpa < drive.min_cgpa:
        return jsonify({"message": "CGPA not eligible"}), 403

    existing = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive.id
    ).first()

    if existing:
        return jsonify({"message": "Already applied"}), 400

    application = Application(student_id=student.id, drive_id=drive.id)

    db.session.add(application)
    db.session.commit()

    cache.clear()

    return jsonify({"message": "Applied successfully"})


@student_bp.route("/applications")
@role_required("student")
def my_applications():

    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message": "Student profile not found"}), 404

    apps = Application.query.filter_by(student_id=student.id).all()

    result = []

    for a in apps:

        drive = Drive.query.get(a.drive_id)
        if drive is None:
            continue

        company = Company.query.get(drive.company_id)
        company_name = company.company_name if company else "Unknown"

        result.append({
            "id": a.id,
            "drive_id": a.drive_id,
            "company": company_name,
            "job_title": drive.job_title if drive else "N/A",
            "status": a.status,
            "application_date": a.application_date,
            "interview_date": a.interview_date.isoformat() if a.interview_date else None
        })

    return jsonify(result)


@student_bp.route("/export")
@role_required("student")
def export():

    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message": "Student profile not found"}), 404

    task = export_student_applications.delay(student.id)

    return jsonify({"task_id": task.id})


@student_bp.route("/search-drives")
@role_required("student")
def search_drives():

    title = request.args.get("title","")

    drives = Drive.query.filter(
        Drive.job_title.contains(title),
        Drive.status == "Approved"
    ).all()

    result = []

    for d in drives:

        company = Company.query.get(d.company_id)

        if not company:
            continue

        result.append({
            "id": d.id,
            "company_name": company.company_name,
            "title": d.job_title,
            "ctc": d.ctc,
            "min_cgpa": d.min_cgpa,
            "deadline": d.deadline
        })

    return jsonify(result)


@student_bp.route("/task-status/<task_id>")
@role_required("student")
def task_status(task_id):
    task = celery.AsyncResult(task_id)
    return jsonify({
        "state": task.state,
        "result": str(task.result),
        "traceback": str(task.traceback) 
    })


@student_bp.route("/update-profile", methods=["PUT"])
@role_required("student")
def update_profile():

    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"message": "Student not found"}), 404

    data = request.get_json()

    student.name = data.get("name", student.name)
    student.branch = data.get("branch", student.branch)
    student.cgpa = data.get("cgpa", student.cgpa)
    student.year = data.get("year", student.year)

    db.session.commit()

    return jsonify({"message": "Profile updated"})


import os
from werkzeug.utils import secure_filename
from flask_jwt_extended import get_jwt_identity

UPLOAD_FOLDER = "uploads/resumes"


@student_bp.route("/upload-resume", methods=["POST"])
@role_required("student")
def upload_resume():

    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first()

    if "resume" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    # PDF restriction
    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"message": "Only PDF resumes are allowed"}), 400

    filename = secure_filename(file.filename)

    filepath = os.path.join("uploads/resumes", filename)

    file.save(filepath)

    student.resume = filename

    db.session.commit()

    return jsonify({"message": "Resume uploaded successfully"})


@student_bp.route("/resume")
@role_required("student")
def get_resume():

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(user_id=user_id).first()

    if not student or not student.resume:
        return jsonify({"message": "No resume found"}), 404

    return send_from_directory("uploads/resumes", student.resume)


@student_bp.route("/resume/<filename>")
def download_resume(filename):
    return send_from_directory("uploads/resumes", filename)


@student_bp.route("/download-export/<int:student_id>")
def download_export(student_id):      # ✅ no @role_required
    filename = f"exports/student_{student_id}.csv"
    if not os.path.exists(filename):
        return jsonify({"message": "Export not ready yet"}), 404
    return send_file(filename, as_attachment=True, download_name="applications.csv")