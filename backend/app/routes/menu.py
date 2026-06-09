from flask import Blueprint, jsonify
from services import obtener_menu_plato_service

menu_bp = Blueprint("menu", __name__)

#permite mostrar los platos en la pantalla de menu
@menu_bp.route("/menu", methods=["GET"])
def ver_menu():
    platos = obtener_menu_plato_service()

    return jsonify(platos), 200