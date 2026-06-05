from flask import Blueprint, request, jsonify
from db import query_db

menu_bp = Blueprint("menu", __name__)

#permite mostrar los platos en la pantalla de menu
@menu_bp.route("/menu", methods=["GET"])
def ver_menu():
    query = "SELECT nombre_plato, descripcion, precio FROM menu WHERE estado = True"
    platos = query_db(query)

    return jsonify(platos), 200