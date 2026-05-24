from flask import Blueprint, jsonify

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/metricas', methods=['GET'])
def get_metricas():
    return jsonify({"mensaje": "Endpoint de Métricas del Dashboard funcionando"})