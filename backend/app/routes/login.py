from flask import Blueprint, jsonify

login_bp = Blueprint('login', __name__, url_prefix='/api/login')

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    return jsonify({"mensaje": "Endpoint de Login funcionando"})
