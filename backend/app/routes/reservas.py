from flask import Blueprint, jsonify

reservas_bp = Blueprint('reservas', __name__, url_prefix='/api/reservas')

@reservas_bp.route('/', methods=['GET'])
def get_reservas():
    return jsonify({"mensaje": "Endpoint de Reservas funcionando"})
