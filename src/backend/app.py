código mejorado CON comentarios educativos
// import Flask
import os
from flask import Flask
# Configuración básica
app = Flask(__name__)
# CORS para todas las rutas /api/*
cors = CORS(app, resources={r"/api/*": {\"origins\": "*"}}, supports_credentials=True)
# JWT Manager
jwt = JWTManager(app)