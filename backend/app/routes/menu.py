from flask import Blueprint, jsonify
from services import obtener_menu_plato_service
from services.admin_menu_service import obtener_menu_admin_service

menu_bp = Blueprint("menu", __name__)

@menu_bp.route("/menu", methods=["GET"]) 
def ver_menu():
    try:
        platos = obtener_menu_admin_service() 
        return jsonify(platos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500