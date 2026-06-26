from flask import Flask, jsonify
from pathlib import Path
from flask_cors import CORS
from dotenv import load_dotenv
import os

base_dir = Path(__file__).resolve().parent
load_dotenv(os.path.join(base_dir, '.env'))

from . import db
from .extensions import mail
from .routes import (
    menu_bp,
    resenas_bp,
    auth_bp,
    reservas_bp,
    servicios_bp,
    admin_menu_bp,
    dashboard_bp
)


def create_app():
    app = Flask(__name__)

    app.config.from_object('api.config')

    CORS(app, origins=[app.config.get('FRONTEND_URL', 'http://localhost:3000')], supports_credentials=True)

    db.init_app(app)
    mail.init_app(app)
    mail.app = app

    app.register_blueprint(menu_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_menu_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp)

    app.register_blueprint(resenas_bp)
    app.register_blueprint(reservas_bp)
    app.register_blueprint(servicios_bp)

    @app.route('/')
    def index():
        return jsonify({"estado": "online", "mensaje": "Backend de Burger funcionando correctamente en el puerto 5000"}), 200

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({"error": "Endpoint no encontrado"}), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({"error": "Error interno del servidor"}), 500

    return app
