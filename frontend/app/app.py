from flask import Flask
from rutas_cliente import cliente_bp
from rutas_admin import admin_bp 

app = Flask(__name__)
app.secret_key = 'burger'
app.register_blueprint(cliente_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run(port=3000, debug=True)