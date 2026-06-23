from flask import Blueprint, jsonify
from services.servicios_service import obtener_total_servicios_activos
from services.reservas_service import obtener_total_reservas_pendientes 
from services.admin_menu_service import obtener_total_platos_activos
from services.resenas_service import obtener_total_resenas_positivas, obtener_total_resenas_negativas
from services.auth_service import obtener_total_usuarios

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/metricas', methods=['GET'])
def get_metricas():
    try:
        total_platos = obtener_total_platos_activos()
        total_reservas = obtener_total_reservas_pendientes()
        total_servicios = obtener_total_servicios_activos() 
        total_res_pos = obtener_total_resenas_positivas()
        total_res_neg = obtener_total_resenas_negativas()
        total_usuarios = obtener_total_usuarios()

        return jsonify({
            "status": "success",
            "data": {
                "total_platos_activos": total_platos,
                "total_reservas_pendientes": total_reservas,
                "total_servicios_activos": total_servicios,
                "total_resenas_positivas": total_res_pos,
                "total_resenas_negativas": total_res_neg,
                "total_usuarios": total_usuarios
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "No se pudieron obtener las métricas del dashboard.",
            "error": str(e)
        }), 500