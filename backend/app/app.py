from flask import Flask, jsonify
from flask_cors import CORS
from routes import menu_bp, reseñas_bp, login_bp, reservas_bp, servicios_bp

def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:3000"])
    # Registro de Blueprints
    app.register_blueprint(menu_bp)
    app.register_blueprint(reseñas_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(reservas_bp)
    app.register_blueprint(servicios_bp)

    # Manejo de errores
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