import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from werkzeug.utils import secure_filename
import requests
from utils import requiere_login, guardar_sesion, limpiar_sesion, extraer_mensajes_error

admin_bp = Blueprint('admin', __name__)
BACKEND_URL = "http://127.0.0.1:5000/api"

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
@requiere_login()
def dashboard():
    try:
        resp_platos = requests.get("http://127.0.0.1:5000/admin/menu/cantidad-platos-activos")
        resp_servicios = requests.get("http://127.0.0.1:5000/api/resenas/admin/cantidad-resenas")

        cant_platos = resp_platos.json().get('cantidad', 0) if resp_platos.status_code == 200 else 0
        cant_servicios = resp_servicios.json().get('cantidad', 0) if resp_servicios.status_code == 200 else 0
        return render_template(
            "gestion/dashboard.html",
            total_platos=cant_platos,
            total_servicios=cant_servicios
        )
    except Exception as e:
        print(f"Error al cargar métricas del dashboard: {e}")
        return "Error interno del servidor", 500

@admin_bp.route("/admin/menu", methods=["GET"])
@requiere_login()
def ver_menu():
    try:
        response = requests.get("http://127.0.0.1:5000/admin/menu")

        platos = []
        if response.status_code == 200:
            platos = response.json()
        else:
            print(f"Advertencia: El Backend devolvió código {response.status_code}")

        return render_template('gestion/menu.html', platos=platos)
    except Exception as e:
        print(f"Error crítico en /admin/menu: {e}")
        return f"Error interno del servidor: {e}", 500
    
@admin_bp.route("/admin/menu/editar/<int:id_plato>", methods=["GET", "POST"])
def editar_plato(id_plato):
    response_get = requests.get(f"http://127.0.0.1:5000/admin/menu/{id_plato}")
    if response_get.status_code != 200:
        return "El plato no existe o el Backend no responde", 404

    plato_data = response_get.json()[0]
    if request.method == "POST":
        data_actualizada = {
            "nombre_plato": request.form.get("nombre_plato"),
            "descripcion": request.form.get("descripcion"),
            "precio": float(request.form.get("precio", 0)),
            "activo": int(request.form.get("activo", 1))  # Usamos 'estado' por consistencia
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
            data_actualizada["imagen"] = plato_data.get("imagen")

        response_put = requests.patch(f"http://127.0.0.1:5000/admin/menu/{id_plato}", json=data_actualizada)

        if response_put.status_code == 200:
            return redirect(url_for('admin.ver_menu'))
        else:
            return f"Error al actualizar el plato en el Backend: {response_put.text}", response_put.status_code

    return render_template('gestion/editar_plato.html', plato=plato_data)

@admin_bp.route('/admin/menu/eliminar/<int:id_plato>', methods=['POST'])
def borrar_plato(id_plato):
    response_post = requests.delete(f"http://127.0.0.1:5000/admin/menu/{id_plato}")
    if response_post.status_code == 200:
        return redirect(url_for("admin.ver_menu"))
    else:
        return f"No se pudo eliminar el plato: {response_post.text}", response_post.status_code


@admin_bp.route("/admin/menu/crear", methods=["GET", "POST"])
def crear_plato():
    if request.method == "POST":
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

                response = requests.post("http://127.0.0.1:5000/admin/menu", json=data)
                if response.status_code == 201:
                    flash('¡Nuevo plato añadido exitosamente!', 'success')
                    return redirect(url_for('admin.ver_menu'))
                else:
                    flash(f'Error del Backend al crear: {response.text}', 'danger')
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
@requiere_login()
def ver_servicios():
    try:
        response = requests.get(f"{BACKEND_URL}/servicios/")
        servicios = response.json() if response.status_code == 200 else []
    except Exception:
        servicios = []
    return render_template('gestion/servicios.html', servicios=servicios)

@admin_bp.route("/admin/dashboard/servicios/crear", methods=["GET"])
def crear_servicio_vista():
    return render_template('gestion/crear_servicio.html')


@admin_bp.route('/admin/dashboard/servicios/editar/<int:id_servicio>/procesar', methods=['POST'])
@requiere_login()
def actualizar_servicio_proceso(id_servicio):
    payload = {
        "nombre": request.form.get("nombre", "").strip(),
        "activo": (request.form.get("activo") == "True")
    }
    try:
        response = requests.patch(f"{BACKEND_URL}/servicios/{id_servicio}", json=payload)
        if response.status_code == 200:
            flash('¡Servicio modificado!', 'success')
        else:
            flash(response.json().get("error", "Error"), "danger")
    except Exception:
        flash("Error al conectar con la API", "danger")
    return redirect(url_for('admin.ver_servicios'))



@admin_bp.route('/admin/dashboard/reservas')
@requiere_login()
def reservas():
    try:
        response = requests.get(f"{BACKEND_URL}/reservas/")
        reservas_lista = response.json() if response.status_code == 200 else []
    except Exception:
        reservas_lista = []
    return render_template('gestion/reservas.html', reservas=reservas_lista)