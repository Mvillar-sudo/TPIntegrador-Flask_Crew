from flask import Flask
from dotenv import load_dotenv
import os
from .rutas_cliente import cliente_bp
from .rutas_admin import admin_bp


app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
app.register_blueprint(cliente_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run(port=3000, debug=True)