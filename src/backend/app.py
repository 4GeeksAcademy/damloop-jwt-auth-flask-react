from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from models import db, User

app = Flask(__name__)

# Configuración básica
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret-key"

db.init_app(app)
Migrate(app, db)
jwt = JWTManager(app)

# CORS para todas las rutas /api/*
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)


# -----------------------------
# RUTA SIGNUP
# -----------------------------
@app.route('/api/signup', methods=['POST', 'OPTIONS'])
def signup():
    if request.method == 'OPTIONS':
        return jsonify({"msg": "ok"}), 200

    email = request.json.get("email")
    password = request.json.get("password")

    if not email or not password:
        return jsonify({"msg": "Email y contraseña requeridos"}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"msg": "El usuario ya existe"}), 400

    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Usuario creado correctamente"}), 201


# -----------------------------
# RUTA LOGIN
# -----------------------------
@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({"msg": "ok"}), 200

    email = request.json.get("email")
    password = request.json.get("password")

    if not email or not password:
        return jsonify({"msg": "Email y contraseña requeridos"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"msg": "Credenciales inválidas"}), 401

    token = create_access_token(identity=email)
    return jsonify({"token": token}), 200


# -----------------------------
# RUTA PRIVADA
# -----------------------------
@app.route('/api/private', methods=['GET'])
@jwt_required()
def private():
    user_email = get_jwt_identity()
    return jsonify({"msg": f"Hola {user_email}, acceso permitido"}), 200


# -----------------------------
# MAIN
# -----------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
