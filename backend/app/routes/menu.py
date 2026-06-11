from flask import Blueprint, jsonify
from services import obtener_menu_plato_service
from services.admin_menu_service import obtener_menu_admin_service

menu_bp = Blueprint("menu", __name__)

@menu_bp.route("/api/menu", methods=["GET"]) # Asegurate de que coincida con tu ruta
def ver_menu():
    try:
        platos = obtener_menu_admin_service() # Trae id_plato, nombre, precio, descripcion, imagen, estado
        return jsonify(platos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500