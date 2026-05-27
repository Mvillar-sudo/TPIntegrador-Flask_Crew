from flask import Blueprint, request, jsonify
from services import post_servicio, get_servicio
servicio_bp = Blueprint('servicios', __name__)

# 1. ENDPOINT PARA MOSTRAR LOS SERVICIOS (GET)
@servicio_bp.route('/api/servicios', methods=['GET'])
def listar_servicios():
    resultados = get_servicio()
    return jsonify(resultados), 200

# 2. ENDPOINT PARA AGREGAR UN SERVICIO (POST)
@servicio_bp.route('/api/servicios', methods=['POST'])
def agregar_servicio():
    datos = request.get_json()
    respuesta_servicio = post_servicio(datos)
    return jsonify({respuesta_servicio}), 201

#3. ENDPOINT PARA ACTUALIZAR UN SERVICIO (PATCH)
@servicio_bp.route('/api/servicios/<int:id>', methods=['PATCH'])
def actualizar_servicio(id):
    datos = request.get_json()
    respuesta_servicio = post_servicio(id, datos)
    return jsonify({respuesta_servicio}), 200