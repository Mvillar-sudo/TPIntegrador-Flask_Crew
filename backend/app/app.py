from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

import db
from extensions import mail

from routes.menu import menu_bp
from routes.resena import resenas_bp
from routes.auth import auth_bp
from routes.reservas import reservas_bp
from routes.servicios import servicios_bp
from routes.admin_menu import admin_menu_bp
from routes.dashboard import dashboard_bp

from config import MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD

def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config['MAIL_SERVER'] = MAIL_SERVER
    app.config['MAIL_PORT'] = MAIL_PORT
    app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD

    CORS(app, origins=["http://localhost:3000"], supports_credentials=True)
    
    db.init_app(app)
    mail.init_app(app)
    mail.app = app

    app.register_blueprint(menu_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(admin_menu_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp, url_prefix='/api')
    
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

if __name__ == '__main__':
    app = create_app()
    app.run(port=5000, debug=True)