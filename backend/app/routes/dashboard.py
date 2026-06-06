from flask import Blueprint, jsonify, session

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.before_request
def verificar_sesion():
    if "usuario" not in session:
        return jsonify({"mensaje": "No autorizado. Inicia sesión primero."}), 401

@dashboard_bp.route('/metricas', methods=['GET'])
def get_metricas():
    return jsonify({"mensaje": "Endpoint de Métricas del Dashboard funcionando"})