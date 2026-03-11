from flask import Flask
from config import Config
from extensions import db, jwt, bcrypt, cache, mail, celery, migrate
from models import User
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.company import company_bp
from routes.student import student_bp
from flask_cors import CORS
from celery_worker import make_celery


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(
        app,
        resources={r"/*": {"origins": "http://localhost:5173"}},
        allow_headers=["Content-Type", "Authorization"],
        supports_credentials=True
    )

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db) 
    make_celery(app) 

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(student_bp)

    @app.route("/")
    def home():
        return "Backend Running"

    return app


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        existing_admin = User.query.filter_by(role="admin").first()
        if not existing_admin:
            hashed = bcrypt.generate_password_hash("Mahi#1323").decode("utf-8")
            admin = User(
                email="mahichoudhary1328@gmail.com",
                password_hash=hashed,
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()

    app.run(debug=True)