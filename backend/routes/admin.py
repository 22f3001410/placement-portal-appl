from flask import Blueprint, jsonify, request
from utils.decorators import role_required
from extensions import db, cache
from models import Student, Company, Drive, Application, User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard", methods=["GET"])
@role_required("admin")
@cache.cached(timeout=60)
def dashboard():
    return jsonify({
        "total_students": Student.query.count(),
        "total_companies": Company.query.count(),
        "total_drives": Drive.query.count()
    })


@admin_bp.route("/approve-company/<int:id>", methods=["PUT"])
@role_required("admin")
def approve_company(id):
    company = Company.query.get(id)
    company.approval_status = "Approved"
    db.session.commit()
    cache.clear()
    return jsonify({"message": "Company approved"})


@admin_bp.route("/reject-company/<int:id>", methods=["PUT"])
@role_required("admin")
def reject_company(id):
    company = Company.query.get(id)
    company.approval_status = "Rejected"
    db.session.commit()
    cache.clear()
    return jsonify({"message": "Company rejected"})


@admin_bp.route("/approve-drive/<int:id>", methods=["PUT"])
@role_required("admin")
def approve_drive(id):
    drive = Drive.query.get(id)
    drive.status = "Approved"
    db.session.commit()
    cache.clear()
    return jsonify({"message": "Drive approved"})


@admin_bp.route("/all-applications", methods=["GET"])
@role_required("admin")
def all_applications():
    apps = Application.query.all()
    return jsonify([
        {
            "id": a.id,
            "student_id": a.student_id,
            "drive_id": a.drive_id,
            "status": a.status
        }
        for a in apps
    ])


@admin_bp.route("/search/students")
@role_required("admin")
def search_students():
    name = request.args.get("name")
    students = Student.query.filter(Student.name.contains(name)).all()
    return jsonify([{"id": s.id, "name": s.name} for s in students])


@admin_bp.route("/search/companies")
@role_required("admin")
def search_companies():
    name = request.args.get("name")

    companies = Company.query.filter(
        Company.company_name.contains(name)
    ).all()

    return jsonify([
        {
            "id": c.id,
            "company_name": c.company_name,
            "approval_status": c.approval_status
        }
        for c in companies
    ])


@admin_bp.route("/reject-drive/<int:id>", methods=["PUT"])
@role_required("admin")
def reject_drive(id):
    drive = Drive.query.get(id)
    drive.status = "Rejected"
    db.session.commit()
    cache.clear()
    return jsonify({"message": "Drive rejected"})


@admin_bp.route("/search/drives")
@role_required("admin")
def search_drives():
    title = request.args.get("title")
    drives = Drive.query.filter(Drive.job_title.contains(title)).all()

    return jsonify([
        {
    "id": d.id,
    "title": d.job_title,
    "status": d.status
}
        for d in drives
    ])

@admin_bp.route("/activate-user/<int:id>", methods=["PUT"])
@role_required("admin")
def activate_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    user.is_active = True
    db.session.commit()

    return jsonify({"message": "User activated"})

@admin_bp.route("/deactivate-user/<int:id>", methods=["PUT"])
@role_required("admin")
def deactivate_user(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    user.is_active = False
    db.session.commit()

    return jsonify({"message": "User deactivated"})

@admin_bp.route("/students")
@role_required("admin")
def get_students():

    students = db.session.query(Student, User)\
        .join(User, Student.user_id == User.id).all()

    return jsonify([
        {
            "id": s.id,
            "user_id": u.id,
            "name": s.name,
            "branch": s.branch,
            "cgpa": s.cgpa,
            "is_active": u.is_active
        }
        for s, u in students
    ])

@admin_bp.route("/companies")
@role_required("admin")
def get_companies():

    companies = db.session.query(Company, User)\
        .join(User, Company.user_id == User.id).all()

    return jsonify([
        {
            "id": c.id,
            "user_id": u.id,
            "company_name": c.company_name,
            "approval_status": c.approval_status,
            "is_active": u.is_active
        }
        for c, u in companies
    ])

@admin_bp.route("/drives")
@role_required("admin")
def get_drives():

    drives = Drive.query.all()

    return jsonify([
        {
            "id": d.id,
            "title": d.job_title,
            "status": d.status
        }
        for d in drives
    ])

@admin_bp.route("/reports")
@role_required("admin")
def reports():

    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_drives = Drive.query.count()

    total_applications = Application.query.count()

    placed_students = Application.query.filter_by(status="Selected").count()

    placement_rate = 0
    if total_students > 0:
        placement_rate = round((placed_students / total_students) * 100, 2)

    return jsonify({
        "total_students": total_students,
        "total_companies": total_companies,
        "total_drives": total_drives,
        "total_applications": total_applications,
        "placed_students": placed_students,
        "placement_rate": placement_rate
    })