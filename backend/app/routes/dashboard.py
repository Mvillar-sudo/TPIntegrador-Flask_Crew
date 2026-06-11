from flask import Blueprint, jsonify
from services.servicios_service import obtener_total_servicios_activos
from services.reservas_service import obtener_total_reservas_pendientes 
from services.admin_menu_service import obtener_total_platos_activos

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/metricas', methods=['GET'])
def get_metricas():
    try:
        total_platos = obtener_total_platos_activos()
        total_reservas = obtener_total_reservas_pendientes()
        total_servicios = obtener_total_servicios_activos() 

        return jsonify({
            "status": "success",
            "data": {
                "total_platos_activos": total_platos,
                "total_reservas_pendientes": total_reservas,
                "total_servicios_activos": total_servicios
            }
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "No se pudieron obtener las métricas del dashboard.",
            "error": str(e)
        }), 500