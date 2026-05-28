from flask import Blueprint, request, jsonify
from services import post_servicio, get_servicio, patch_servicio
from validators import validar_servicio
servicio_bp = Blueprint('servicios', __name__)

# 1. ENDPOINT PARA MOSTRAR LOS SERVICIOS (GET)
@servicio_bp.route('/api/servicios', methods=['GET'])
def listar_servicios():
    """Retorna la lista completa de servicios extras ordenados por nombre.
    
    Returns:
        JSON: Lista de servicios con código 200.
    """
    resultados = get_servicio()
    return jsonify(resultados), 200

# 2. ENDPOINT PARA AGREGAR UN SERVICIO (POST)
@servicio_bp.route('/api/servicios', methods=['POST'])
def agregar_servicio():
    """Crea un nuevo servicio extra. Valida los datos antes de insertarlos.
    
    Body JSON:
        nombre (str): Nombre del servicio. Obligatorio, máx 50 caracteres.
        descripcion (str): Descripción del servicio. Opcional, máx 100 caracteres.
    
    Returns:
        JSON: Mensaje de confirmación con código 201, o errores de validación con código 400.
    """
    datos = request.get_json()
    
    # Validar
    errores = validar_servicio(datos)
    if errores:
        return jsonify({"errores": errores}), 400

    respuesta_servicio = post_servicio(datos)
    return jsonify(respuesta_servicio), 201

#3. ENDPOINT PARA ACTUALIZAR UN SERVICIO (PATCH)
@servicio_bp.route('/api/servicios/<int:id>', methods=['PATCH'])
def actualizar_servicio(id):
    """Actualiza parcialmente un servicio extra existente.
    
    Args:
        id (int): ID del servicio a actualizar.
    
    Body JSON (todos opcionales):
        nombre (str): Nuevo nombre. Máx 50 caracteres.
        descripcion (str): Nueva descripción. Máx 100 caracteres.
        activo (bool): Estado del servicio (true/false).
    
    Returns:
        JSON: Mensaje de confirmación con código 200, o errores de validación con código 400.
    """
    datos = request.get_json()

    # Validar
    errores = validar_servicio(datos, es_actualizacion=True)
    if errores:
        return jsonify({"errores": errores}), 400

    respuesta_servicio = patch_servicio(id, datos)
    return jsonify(respuesta_servicio), 200