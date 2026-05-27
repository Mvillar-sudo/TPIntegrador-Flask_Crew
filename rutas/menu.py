from flask import Blueprint, request, jsonify
from db import get_connection

menu_bp = Blueprint("menu", __name__)

#permite mostrar los platos en la pantalla de menu
@menu_bp.route("/menu", methods=["GET"])
def mostrar_plato():
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute(
        "SELECT nombre_plato, descripcion, precio FROM menu WHERE estado = True",
    )

    platos = cursor.fetchall()

    cursor.close()
    conn.close()

    
    return jsonify(platos), 200