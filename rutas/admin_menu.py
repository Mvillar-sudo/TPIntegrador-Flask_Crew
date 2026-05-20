from flask import Blueprint, request, jsonify
from db import get_connection

admin_menu_bp = Blueprint("admin_menu", __name__)

#para que el admin pueda crear un plato
@admin_menu_bp.route("/admin/menu", methods=["POST"])
def crear_plato():

    data = request.json
    nombre = data["nombre_plato"]
    descripcion = data["descripcion"]
    precio = data["precio"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO menu (nombre_plato, descripcion, precio, estado)
        VALUES (%s, %s, %s, true)
    """, (nombre, descripcion, precio))

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensaje": "Plato creado correctamente"}, 201


#le permite al admin ver todos los platos del menu
@admin_menu_bp.route("/admin/menu", methods=["GET"])
def ver_menu_admin():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM menu")

    platos = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(platos), 200



#para que el admin pueda ver los detalles de un plato en especifico
@admin_menu_bp.route("/admin/menu/<int:id_plato>", methods=["GET"])
def ver_plato(id_plato):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM menu WHERE id_plato = %s", (id_plato,))
    plato = cursor.fetchone()

    cursor.close()
    conn.close()

    if not plato:
        return {"mensaje": "Plato no encontrado"}, 404

    return jsonify(plato), 200



#le permite al admin modificar completamente los datos de un plato
@admin_menu_bp.route("/admin/menu/<int:id_plato>", methods=["PUT"])
def modificar_platos(id_plato):

    data = request.json
    nombre = data["nombre_plato"]
    descripcion = data["descripcion"]
    precio = data["precio"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE menu
        SET nombre_plato = %s,
            descripcion = %s,
            precio = %s
        WHERE id_plato = %s
    """, (nombre, descripcion, precio, id_plato))

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensaje": "Plato actualizado correctamente"}, 200



#le permite al admin modificar uno o más datos de un plato
@admin_menu_bp.route("/admin/menu/<int:id_plato>", methods=["PATCH"])
def actualizar_plato(id_plato):

    data = request.json

    if not data:
        return {"mensaje": "No se enviaron datos"}, 400

    conn = get_connection()
    cursor = conn.cursor()

    if "nombre_plato" in data:
        cursor.execute(
            "UPDATE menu SET nombre_plato = %s WHERE id_plato = %s",
            (data["nombre_plato"], id_plato)
        )

    if "descripcion" in data:
        cursor.execute(
            "UPDATE menu SET descripcion = %s WHERE id_plato = %s",
            (data["descripcion"], id_plato)
        )

    if "precio" in data:
        cursor.execute(
            "UPDATE menu SET precio = %s WHERE id_plato = %s",
            (data["precio"], id_plato)
        )
    

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensaje": "Plato actualizado"}, 200


#para que el admin pueda desactivar o activar la visibilización de un plato
@admin_menu_bp.route("/admin/menu/<int:id_plato>/estado", methods=["PATCH"])
def cambiar_estado(id_plato):

    data = request.json
    estado = data["estado"]  # true o false

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE menu SET estado = %s WHERE id_plato = %s",
        (estado, id_plato)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {"mensaje": "Estado actualizado"}, 200




#para que el admin pueda eliminar un plato de la base de datos
@admin_menu_bp.route("/admin/menu/<int:id_plato>", methods=["DELETE"])
def eliminar_plato(id_plato):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM menu WHERE id_plato = %s",
        (id_plato,)
    )
    
    conn.commit()

    cursor.close()
    conn.close()

    return {"mensaje": "Plato eliminado correctamente"}, 200

