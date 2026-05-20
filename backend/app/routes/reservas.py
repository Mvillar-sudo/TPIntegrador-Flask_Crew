from flask import Blueprint, jsonify

reservas_bp = Blueprint('reservas', __name__, url_prefix='/api/reservas')

@reservas_bp.route('/', methods=['GET'])
def get_reservas():
    return jsonify({"mensaje": "Endpoint de Reservas funcionando"})

@reservas_bp.route('/<int: id_reserva>', methods=['GET'])
def get_reserva(id_reserva):
    return jsonify({"mensaje": "Endpoint de Reservas funcionando"})

@reservas_bp.route('/', methods=['POST'])
def crear_reserva():
    return jsonify({"mensaje": "Endpoint de Reservas funcionando"})

@reservas_bp.route('/<int: id_reserva>', methods=['PUT'])
def modificar_reserva(id_reserva):
    return jsonify({"mensaje": "Endpoint de Reservas funcionando"})