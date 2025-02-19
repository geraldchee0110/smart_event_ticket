from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://user:password@db/userdb"
    app.config["JWT_SECRET_KEY"] = "supersecret"
    
    db.init_app(app)
    JWTManager(app)

    from app.routes import user_bp
    app.register_blueprint(user_bp, url_prefix="/users")

    return app