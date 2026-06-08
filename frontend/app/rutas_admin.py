from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from backend.app.routes.auth import auth_bp
from backend.app.routes.admin_menu import admin_menu_bp
from backend.app.routes.servicios import servicios_bp
from backend.app.services.servicios_service import (obtener_servicios, obtener_servicio_id, crear_servicio_db, actualizar_servicio_db, eliminar_servicio_db)
from backend.app.services.admin_menu_service import (obtener_menu_admin_service, obtener_plato_service, cambiar_estado_plato_service, actualizar_parcial_plato_service, eliminar_plato_service, crear_plato_service)
from backend.app.db import query_db, execute_db
from backend.app.validators.admin_menu_validator import (validar_crear_plato, validar_id_plato)
from backend.app.validators.servicios_validator import (validar_servicio)

import requests

admin_bp = Blueprint('admin', __name__)

admin_bp.register_blueprint(auth_bp)
admin_bp.register_blueprint(admin_menu_bp)
admin_bp.register_blueprint(servicios_bp)

@admin_bp.route('/admin/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = {
            "usuario": request.form.get("usuario"),
            "password": request.form.get("password")
        }
        response = requests.post("http://127.0.0.1:5000/login", json=data)
        respuesta = response.json()
        if response.status_code == 200:
            session['admin_logeado'] = True
            session['usuario'] = respuesta.get('usuario')
            return redirect(url_for('admin.dashboard'))

        return render_template('gestion/login.html', error=respuesta.get("mensaje"))

    return render_template('gestion/login.html')

@admin_bp.route('/admin/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.login'))

@admin_bp.route('/admin/dashboard')
def dashboard():
    if not session.get('admin_logeado'):
        return redirect(url_for('admin.login'))
        
    return render_template('gestion/dashboard.html')

@admin_bp.route("/admin/menu", methods=["GET"])
def ver_menu():
    try:
        platos = obtener_menu_admin_service()

        return render_template('gestion/menu.html', platos=platos)
    except Exception as e:
        print(f"Error crítico en /admin/menu: {e}")
        return f"Error interno del servidor: {e}", 500
    
@admin_bp.route("/admin/menu/editar/<int:id_plato>", methods=["GET", "POST"])
def editar_plato(id_plato):
    if request.method == "POST":
        data_actualizada = {
            "nombre_plato": request.form.get("nombre_plato"),
            "descripcion": request.form.get("descripcion"),
            "precio": float(request.form.get("precio", 0)),
            "estado": int(request.form.get("estado", 1))
        }
        
        exito = actualizar_parcial_plato_service(id_plato, data_actualizada)
        
        if exito:
            return redirect(url_for('admin.ver_menu'))
        else:
            return "El plato no existe o fue eliminado por otro usuario", 404

    plato = obtener_plato_service(id_plato)
    if not plato:
        return "Plato no encontrado", 404
        
    return render_template('gestion/editar_plato.html', plato=plato)

@admin_bp.route('/admin/menu/eliminar/<int:id_plato>', methods=['POST'])
def borrar_plato(id_plato):

    eliminado = eliminar_plato_service(id_plato)

    if not eliminado:
        return "Plato no eliminado", 404

    return redirect(url_for("admin.ver_menu"))


@admin_bp.route("/admin/menu/crear", methods=["GET"])
def crear_plato_vista():
    return render_template('gestion/crear_plato.html')

@admin_bp.route("/admin/menu/crear_proceso", methods=["POST"])
def crear_plato_proceso():
    data = {
        "nombre_plato": request.form.get("nombre_plato"),
        "descripcion": request.form.get("descripcion"),
        "precio": float(request.form.get("precio", 0))
    }
    crear_plato_service(data)
    flash('¡Nuevo plato añadido exitosamente!', 'success')
    return redirect(url_for('admin.ver_menu'))

@admin_bp.route('/admin/dashboard/reservas')
def reservas():
    if not session.get('admin_logeado'): 
        return redirect(url_for('admin.login'))
        
    reservas_lista = [
        {
            "id": 101, 
            "email": "juan@email.com", 
            "fecha": "2026-05-28", 
            "hora": "21:00", 
            "cantidad_personas": 4, 
            "estado": "Confirmada",
            "token_cancelacion": "xyz789token",
            "qr_code": "qr_reserva_101.png",
            "fecha_creacion": "2026-05-25"
        }
    ]
    return render_template('gestion/reservas.html', reservas=reservas_lista)


@admin_bp.route('/admin/dashboard/servicios')
def ver_servicios():
    if not session.get('admin_logeado'): 
        return redirect(url_for('admin.login'))
    try:
        servicios = obtener_servicios()
        return render_template('gestion/servicios.html', servicios=servicios)
    except RuntimeError as e:
        return "No se encontro el abm", 500 
    
@admin_bp.route("/admin/dashboard/servicios/crear", methods=["GET"])
def crear_servicio_vista():
    return render_template('gestion/crear_servicio.html')


@admin_bp.route('/admin/dashboard/servicios/crear_proceso', methods=['POST'])
def crear_servicio_proceso():
    try:
        data = {"nombre": request.form.get("nombre")}

        crear_servicio_db(data)

        return redirect(url_for('admin.ver_servicios'))

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500 
       
@admin_bp.route('/admin/dashboard/servicios/editar/<int:id_servicio>', methods=['GET', 'POST']) # 👈 Soporta ambos métodos
def actualizar_servicio_proceso(id_servicio):
    try:
        servicio = obtener_servicio_id(id_servicio)
        if not servicio:
            flash('Servicio no encontrado', 'danger')
            return redirect(url_for('admin.ver_servicios'))

        estado_real = 1 if request.form.get("activo") else 0
        if request.method == "POST":
            data = {
                "nombre": request.form.get("nombre"),
                "activo": estado_real
            }

            
            error = validar_servicio(data, es_actualizacion=True)
            if error:
                flash(f"Error de validación: {error}", "danger")
                return render_template("gestion/editar_servicio.html", servicio=servicio), 400
            
            actualizar_servicio_db(id_servicio, data)
            
            flash('¡Servicio actualizado con éxito!', 'success')
            return redirect(url_for('admin.ver_servicios'))

        return render_template("gestion/editar_servicio.html", servicio=servicio)

    except Exception as e:
        print(f"Error crítico en controlador de servicios: {e}")
        return "Error interno del servidor", 500
    
@admin_bp.route('/<int:id_servicio>', methods=['POST'])
def eliminar_servicio(id_servicio):
    try:
        filas = eliminar_servicio_db(id_servicio)

        if filas == 0:
            return jsonify({
                "error": "Servicio no encontrado"
            }), 404

        return redirect(url_for('admin.ver_servicios'))

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500