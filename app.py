from flask import Flask
from routes.auth import auth_bp
from routes.admin_menu import admin_menu_bp
from routes.menu import menu_bp

app = Flask(__name__)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_menu_bp)
app.register_blueprint(menu.bp)

if __name__ == "__main__":
    app.run(debug=True)




