from flask import Blueprint, request, jsonify
from ..validators import validar_id_plato, validar_crear_plato
from ..services import (
    crear_plato_service,
    obtener_menu_admin_service,
    obtener_plato_service,
    actualizar_parcial_plato_service,
    cambiar_estado_plato_service,
    eliminar_plato_service,
    obtener_total_platos_activos_service)

admin_menu_bp = Blueprint("admin_menu", __name__)

#para que el admin pueda crear un plato
@admin_menu_bp.route("/admin/menu", methods=["POST"])
def crear_plato():

    data = request.json

    error = validar_crear_plato(data)

    if error:
        return jsonify({"mensaje": error}), 400

    crear_plato_service(data)

    return jsonify({"mensaje": "Plato creado"}), 201

#le permite al admin ver todos los platos del menu
@admin_menu_bp.route("/admin/menu", methods=["GET"])
def ver_menu_admin():

    platos = obtener_menu_admin_service()

    return jsonify(platos), 200

#para que el admin pueda ver los detalles de un plato en especifico
@admin_menu_bp.route("/admin/menu/<int:id_plato>", methods=["GET", "PATCH", "DELETE"])
def gestionar_plato(id_plato):
    error = validar_id_plato(id_plato)
    if error:
        return jsonify({"mensaje": error}), 400

    if request.method == "GET":

        plato = obtener_plato_service(id_plato)
   
        if not plato:
            return jsonify({"mensaje": "Plato no encontrado"}), 404

        return jsonify(plato), 200

    if request.method == "PATCH":
        data = request.json
        if not data:
            return jsonify({"mensaje": "No se enviaron datos"}), 400

        error = validar_id_plato(id_plato)
        if error:
            return jsonify({"mensaje": error}), 400

        actualizado = actualizar_parcial_plato_service(id_plato, data)

        if not actualizado:
            return jsonify({"mensaje": "Plato no encontrado"}), 404

        return jsonify({"mensaje": "Plato actualizado"}), 200

    if request.method == "DELETE":
        eliminado = eliminar_plato_service(id_plato)

        if not eliminado:
            return jsonify({"mensaje": "Plato no encontrado"}), 404

        return jsonify({"mensaje": "Plato eliminado correctamente"}), 200


#para que el admin pueda desactivar o activar la visibilización de un plato
@admin_menu_bp.route("/admin/menu/<int:id_plato>/estado", methods=["PATCH"])
def cambiar_estado(id_plato):

    data = request.json
  
    if not data or "estado" not in data:
        return jsonify({"mensaje": "Falta el campo estado"}), 400

    error = validar_id_plato(id_plato)
    if error:
        return jsonify({"mensaje": error}), 400

    actualizado = cambiar_estado_plato_service(id_plato, data["estado"])

    if not actualizado:
        return jsonify({"mensaje": "Plato no encontrado"}), 404

    return jsonify({"mensaje": "Estado actualizado"}), 200

@admin_menu_bp.route("/admin/menu/cantidad-platos-activos", methods=["GET"])
def obtener_cantidad_platos_activos():
    resultado = obtener_total_platos_activos_service()
    return jsonify({"cantidad": resultado}), 200