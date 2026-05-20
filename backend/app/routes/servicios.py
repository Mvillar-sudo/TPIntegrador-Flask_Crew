from flask import Blueprint, jsonify

servicios_bp = Blueprint('servicios', __name__, url_prefix='/api/servicios')

@servicios_bp.route('/', methods=['GET'])
def get_servicios():
    return jsonify({"mensaje": "Endpoint de Servicios funcionando"})

@servicios_bp.route('/<int: id_servicio>', methods=['GET'])
def get_servicio(id_servicio):
    return jsonify({"mensaje": "Endpoint de servicios funcionando"})

@servicios_bp.route('/', methods=['POST'])
def crear_servicio():
    return jsonify({"mensaje": "Endpoint de servicios funcionando"})

@servicios_bp.route('/<int: id_servicio>', methods=['PUT'])
def modificar_servicio(id_servicio):
    return jsonify({"mensaje": "Endpoint de servicios funcionando"})