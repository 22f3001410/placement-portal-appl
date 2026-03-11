from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_mail import Mail
from celery import Celery
from flask_migrate import Migrate 

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
cache = Cache()
mail = Mail()
celery = Celery(
    "placement_portal",
    broker="redis://localhost:6379/0",       
    backend="redis://localhost:6379/0"       
)
migrate = Migrate() 