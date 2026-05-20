from flask import Blueprint, jsonify

reseñas_bp = Blueprint('reseñas', __name__, url_prefix='/api/resenas')

@reseñas_bp.route('/', methods=['GET'])
def get_resenas():
    return jsonify({"mensaje": "Endpoint de Reseñas funcionando"})

@reseñas_bp.route('/<int:id_resena>', methods=['GET'])
def get_resena(id_resena): 
    return jsonify({"mensaje": "Endpoint de reseña encontrado"}) 

@reseñas_bp.route('/', methods=['POST'])
def crear_resena(): 
    return jsonify({"mensaje": "reseña creado"}) 

@reseñas_bp.route('/<int:id_resena>', methods=['PUT'])
def modificar_resena(id_resena): 
    return jsonify({"mensaje": "Endpoint de reseña modificado"})
