from flask import Blueprint, current_app, render_template, request, jsonify, redirect, url_for, session, flash
from backend.app.routes.auth import auth_bp
from backend.app.routes.admin_menu import admin_menu_bp
from backend.app.routes.servicios import servicios_bp
from backend.app.services.servicios_service import (obtener_servicios, obtener_servicio_id, crear_servicio_db, actualizar_servicio_db, eliminar_servicio_db)
from backend.app.services.admin_menu_service import (obtener_menu_admin_service, obtener_plato_service, cambiar_estado_plato_service, actualizar_parcial_plato_service, eliminar_plato_service, crear_plato_service)
from backend.app.db import query_db, execute_db
from backend.app.validators.admin_menu_validator import (validar_crear_plato, validar_id_plato)
from backend.app.validators.servicios_validator import (validar_servicio)
import os
from werkzeug.utils import secure_filename
import requests

admin_bp = Blueprint('admin', __name__)

admin_bp.register_blueprint(auth_bp)
admin_bp.register_blueprint(admin_menu_bp)
admin_bp.register_blueprint(servicios_bp)

@admin_bp.route('/admin/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = {
            "username": request.form.get("username"),
            "password": request.form.get("password")
        }
        response = requests.post("http://127.0.0.1:5000/login", json=data)


        try:
            respuesta = response.json()
        except Exception:
            return render_template(
                'gestion/login.html',
                error="Error inesperado del servidor"
            )

        if response.status_code == 200:
            guardar_sesion(respuesta.get('token'), respuesta.get('usuario'))
            session['admin_logeado'] = True
            return redirect(url_for('admin.dashboard'))

        error_api = respuesta.get("mensaje") if respuesta else "Usuario o contraseña incorrectos"
        return render_template('gestion/login.html', error=error_api)

    return render_template('gestion/login.html')


@admin_bp.route('/admin/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.login'))

@admin_bp.route('/admin/dashboard')
def dashboard():
    if not session.get('admin_logeado'):
        return redirect(url_for('admin.login'))
    try:
        total_platos = obtener_total_platos_activos()
        total_servicios = obtener_total_servicios_activos()

        return render_template(
            "gestion/dashboard.html",
            total_platos=total_platos,
            total_servicios=total_servicios
        )
    except Exception as e:
        print(f"Error al cargar métricas del dashboard: {e}")
        return "Error interno del servidor", 500

@admin_bp.route("/admin/menu", methods=["GET"])
def ver_menu():
    if not session.get('admin_logeado'):
        return redirect(url_for('admin.login'))
    try:
        platos = obtener_menu_admin_service()

        return render_template('gestion/menu.html', platos=platos)
    except Exception as e:
        print(f"Error crítico en /admin/menu: {e}")
        return f"Error interno del servidor: {e}", 500
    
@admin_bp.route("/admin/menu/editar/<int:id_plato>", methods=["GET", "POST"])
def editar_plato(id_plato):
    plato = obtener_plato_service(id_plato)
    if not plato:
        return "Plato no encontrado", 404

    if request.method == "POST":
        data_actualizada = {
            "nombre_plato": request.form.get("nombre_plato"),
            "descripcion": request.form.get("descripcion"),
            "precio": float(request.form.get("precio", 0)),
            "estado": int(request.form.get("estado", 1))
        }

        file = request.files.get("imagen")

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(current_app.root_path, 'static', 'img')

            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)

            data_actualizada["imagen"] = filename
        else:
            data_actualizada["imagen"] = plato.get("imagen")

        exito = actualizar_parcial_plato_service(id_plato, data_actualizada)
        
        if exito:
            return redirect(url_for('admin.ver_menu'))
        else:
            return "El plato no existe o fue eliminado", 404
        
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
    try:
        data = {
            "nombre_plato": request.form.get("nombre_plato", "").strip(),
            "descripcion": request.form.get("descripcion", "").strip(),
            "imagen": None,
            "precio": float(request.form.get("precio", 0))
        }

        file = request.files.get("imagen")

        if file and file.filename != '':
            filename = secure_filename(file.filename)

            upload_folder = os.path.join(current_app.root_path, 'static', 'img')

            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)

            data["imagen"] = filename

        crear_plato_service(data)

        flash('¡Nuevo plato añadido exitosamente!', 'success')
        return redirect(url_for('admin.ver_menu'))

    except Exception as e:
        print(f"Error al crear el plato: {e}")
        flash('Ocurrió un error al procesar el plato.', 'danger')
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

@admin_bp.route('/admin/dashboard/servicios/editar/<int:id_servicio>', methods=['GET'])
def editar_servicio_vista(id_servicio):
    try:
        servicio = obtener_servicio_id(id_servicio)
        if not servicio:
            flash('Servicio no encontrado', 'danger')
            return redirect(url_for('admin.ver_servicios'))

        return render_template("gestion/editar_servicio.html", servicio=servicio)

    except Exception as e:
        print(f"Error al renderizar vista de edición de servicio: {e}")
        return "Error interno del servidor", 500

@admin_bp.route('/admin/dashboard/servicios/editar/<int:id_servicio>/procesar', methods=['POST'])
def actualizar_servicio_proceso(id_servicio):
    try:
        servicio = obtener_servicio_id(id_servicio)
        if not servicio:
            flash('Servicio no encontrado', 'danger')
            return redirect(url_for('admin.ver_servicios'))

        valor_select = request.form.get("activo")

        estado_booleano = (valor_select == "True")

        data = {
            "nombre": request.form.get("nombre", "").strip(),
            "activo": estado_booleano
        }


        error = validar_servicio(data, es_actualizacion=True)
        if error:
            flash(f"Error de validación: {error}", "danger")
            servicio.nombre = data["nombre"]
            servicio.activo = 1 if estado_booleano else 0
            return render_template("gestion/editar_servicio.html", servicio=servicio), 400

        actualizar_servicio_db(id_servicio, data)

        flash('¡Servicio actualizado con éxito!', 'success')
        return redirect(url_for('admin.ver_servicios'))

    except Exception as e:
        print(f"Error crítico en el procesamiento del servicio: {e}")
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