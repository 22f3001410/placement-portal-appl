from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from extensions import db, bcrypt
from models import User, Student, Company

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register/student", methods=["POST"])
def register_student():
    data = request.get_json()

    existing = User.query.filter_by(email=data["email"]).first()
    if existing:
        return jsonify({"message": "Email already registered"}), 400

    hashed = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    user = User(email=data["email"], password_hash=hashed, role="student")
    db.session.add(user)
    db.session.commit()

    student = Student(
        user_id=user.id,
        name=data["name"],
        branch=data["branch"],
        cgpa=data["cgpa"],
        year=data["year"]
    )
    db.session.add(student)
    db.session.commit()

    return jsonify({"message": "Student registered"})


@auth_bp.route("/register/company", methods=["POST"])
def register_company():
    data = request.get_json()

    existing = User.query.filter_by(email=data["email"]).first()
    if existing:
        return jsonify({"message": "Email already registered"}), 400

    hashed = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    user = User(email=data["email"], password_hash=hashed, role="company")
    db.session.add(user)
    db.session.commit()

    company = Company(
        user_id=user.id,
        company_name=data["company_name"],
        hr_contact=data["hr_contact"],
        website=data["website"]
    )
    db.session.add(company)
    db.session.commit()

    return jsonify({"message": "Company registered. Await admin approval."})


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data["email"]).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not bcrypt.check_password_hash(user.password_hash, data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    if not user.is_active:
        return jsonify({"message": "Account is deactivated by admin"}), 403

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )

    return jsonify({"access_token": token})