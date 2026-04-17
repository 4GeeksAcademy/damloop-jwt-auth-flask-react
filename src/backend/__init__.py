from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .models import db

def create_app():
    app = Flask(__name__)

    # Configuración
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret-key"

    # Inicializar extensiones
    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    # ⭐ CORS CORRECTO
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Registrar rutas con prefijo /api
    from .routes import api
    app.register_blueprint(api, url_prefix="/api")

    return app
