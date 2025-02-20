from flask import Flask
from flask_jwt_extended import JWTManager
from supabase import create_client
from app.config import Config

supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt.init_app(app)  # Initialize JWT
    
    from app.routes import user_bp
    app.register_blueprint(user_bp, url_prefix="/users")

    return app