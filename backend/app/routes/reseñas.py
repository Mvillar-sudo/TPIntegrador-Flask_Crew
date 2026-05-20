from flask import Blueprint, jsonify

reseñas_bp = Blueprint('reseñas', __name__, url_prefix='/api/resenas')

@reseñas_bp.route('/', methods=['GET'])
def get_resenas():
    return jsonify({"mensaje": "Endpoint de Reseñas funcionando"})
