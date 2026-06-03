from flask import Flask, jsonify
from flask_cors import CORS
from flask_mail import Mail
from .routes import menu_bp, reseñas_bp, auth_bp, reservas_bp, servicios_bp, dashboard_bp
from .config import MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD
from . import db
from . import mail

def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:3000"])

    # configuración del mail
    app.config['MAIL_SERVER'] = MAIL_SERVER
    app.config['MAIL_PORT'] = MAIL_PORT
    app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD

    # inicializar extensiones
    db.init_app(app)
    mail.init_app(app)

    # registro de blueprints
    app.register_blueprint(menu_bp)
    app.register_blueprint(reseñas_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(reservas_bp)
    app.register_blueprint(servicios_bp)
    app.register_blueprint(dashboard_bp)

    @app.route('/')
    def index():
        return 'Backend funcionando correctamente en el puerto 5000'

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