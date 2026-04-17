from flask import Blueprint, jsonify, request
from .models import User, db
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

api = Blueprint("api", __name__)

# -----------------------------
# HELLO
# -----------------------------
@api.route("/hello")
def hello():
    return jsonify({"msg": "Hello from Flask!"})


# -----------------------------
# SIGNUP
# -----------------------------
@api.route('/signup', methods=['POST', 'OPTIONS'])
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
# LOGIN
# -----------------------------
@api.route('/login', methods=['POST', 'OPTIONS'])
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
# PRIVATE
# -----------------------------
@api.route('/private', methods=['GET'])
@jwt_required()
def private():
    user_email = get_jwt_identity()
    return jsonify({"msg": f"Hola {user_email}, acceso permitido"}), 200
