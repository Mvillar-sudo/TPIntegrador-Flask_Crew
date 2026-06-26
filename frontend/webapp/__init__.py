import os
from flask import Flask
from dotenv import load_dotenv

# Cargar variables de entorno antes de importar blueprints
load_dotenv()

from .rutas_cliente import cliente_bp
from .rutas_admin import admin_bp



def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('FRONTEND_SECRET_KEY', 'burger_secret_frontend_key')

    app.register_blueprint(cliente_bp)
    app.register_blueprint(admin_bp)

    return app
