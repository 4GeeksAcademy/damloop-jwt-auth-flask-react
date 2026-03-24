from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from .extensions import db, jwt, bcrypt
from .models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

# CONFIG
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["JWT_SECRET_KEY"] = "super-secret-key"

# CORS para permitir peticiones desde el frontend (5173)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# INIT EXTENSIONS
db.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)
Migrate(app, db)

# -----------------------------
# SIGNUP
# -----------------------------


@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"msg": "Email y password requeridos"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Usuario ya existe"}), 400

    user = User(email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "Usuario creado"}), 201


# -----------------------------
# LOGIN
# -----------------------------
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Credenciales inválidas"}), 401

    token = create_access_token(identity=user.id)
    return jsonify({"access_token": token}), 200


# -----------------------------
# PRIVATE ROUTE
# -----------------------------
@app.route("/api/private", methods=["GET"])
@jwt_required()
def private():
    user_id = get_jwt_identity()
    return jsonify({"msg": "Acceso permitido", "user_id": user_id}), 200


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
