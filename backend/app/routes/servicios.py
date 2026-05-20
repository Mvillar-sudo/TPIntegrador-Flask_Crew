from flask import Blueprint, jsonify

servicios_bp = Blueprint('servicios', __name__, url_prefix='/api/servicios')

@servicios_bp.route('/', methods=['GET'])
def get_servicios():
    return jsonify({"mensaje": "Endpoint de Servicios funcionando"})
