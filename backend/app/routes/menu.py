from flask import Blueprint, jsonify

menu_bp = Blueprint('menu', __name__, url_prefix='/api/menu')

@menu_bp.route('/', methods=['GET'])
def get_menu():
    return jsonify({"mensaje": "Endpoint de Menú funcionando"})
