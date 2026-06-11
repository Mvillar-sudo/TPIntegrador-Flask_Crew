import requests
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from werkzeug.utils import secure_filename

from utils import requiere_login, guardar_sesion, limpiar_sesion, extraer_mensajes_error

admin_bp = Blueprint('admin', __name__)

BACKEND_URL = "http://127.0.0.1:5000/api"

@admin_bp.route('/admin/login', methods=['GET'])
def login():
    return render_template('gestion/login.html')


@admin_bp.route('/admin/login_process', methods=['POST'])
def login_process():
    payload = {
        "username": request.form.get('username'),
        "password": request.form.get('password')
    }
    try:
        response = requests.post(f"{BACKEND_URL}/login", json=payload)
        res_data = response.json()

        if response.status_code == 200:
            guardar_sesion(res_data.get("token"), {"nombre": res_data.get("usuario")})
            flash("¡Bienvenido al panel!", "success")
            return redirect(url_for('admin.dashboard'))
        else:
            errores = extraer_mensajes_error(res_data)
            flash(errores[0], "danger")
            return redirect(url_for('admin.login'))
    except Exception:
        flash("Error: No se pudo conectar con el servidor de autenticación.", "danger")
        return redirect(url_for('admin.login'))


@admin_bp.route('/admin/logout')
def logout():
    limpiar_sesion()
    flash("Sesión cerrada.", "info")
    return redirect(url_for('admin.login'))


@admin_bp.route('/admin/dashboard')
@requiere_login()
def dashboard():
    try:
        response = requests.get(f"{BACKEND_URL}/dashboard/metricas")
        data = response.json() if response.status_code == 200 else {}
        total_platos = data.get("total_platos", 0)
        total_servicios = data.get("total_servicios", 0)
    except Exception:
        total_platos, total_servicios = 0, 0

    return render_template('gestion/dashboard.html', total_platos=total_platos, total_servicios=total_servicios)


@admin_bp.route("/admin/menu", methods=["GET"])
@requiere_login()
def ver_menu():
    # Aseguramos usar la IP numérica directa para evitar problemas de IPv6
    BACKEND_URL = "http://127.0.0.1:5000/api"
    
    try:
        # Probamos pegarle a la ruta de la API del backend
        response = requests.get(f"{BACKEND_URL}/menu")
        
        # SI DA 404, probamos con la ruta alternativa por si acaso tu backend usa /admin/menu
        if response.status_code == 404:
            response = requests.get(f"{BACKEND_URL}/admin/menu")

        print(f"--- STATUS BACKEND MENU: {response.status_code} ---")
        print(f"--- DATOS RECIBIDOS: {response.text} ---")

        if response.status_code == 200:
            platos = response.json() 
            if platos and len(platos) > 0:
                print("¡¡¡ AQUÍ ESTÁN LAS CLAVES REALES !!! ->", platos[0].keys())
                print("PRIMER PLATO COMPLETO ->", platos[0])
        else:
            platos = []
            
    except Exception as e:
        print(f"--- ERROR AL CONECTAR AL MENU: {e} ---")
        platos = []
        
    return render_template('gestion/menu.html', platos=platos)

@admin_bp.route("/admin/menu/crear", methods=["GET"])
def crear_plato_vista():
    return render_template('gestion/crear_plato.html')

@admin_bp.route("/admin/menu/crear_proceso", methods=["POST"])
@requiere_login()
def crear_plato_proceso():
    try:
        filename = None
        file = request.files.get("imagen")
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(current_app.root_path, 'static', 'img')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            file.save(os.path.join(upload_folder, filename))

        payload = {
            "nombre_plato": request.form.get("nombre_plato", "").strip(),
            "descripcion": request.form.get("descripcion", "").strip(),
            "imagen": filename,
            "precio": float(request.form.get("precio", 0))
        }

        response = requests.post(f"{BACKEND_URL}/admin/menu", json=payload)
        if response.status_code == 201:
            flash('¡Plato añadido exitosamente!', 'success')
        else:
            flash(response.json().get("mensaje", "Error al crear"), 'danger')
    except Exception as e:
        flash(f'Error al procesar: {e}', 'danger')
    return redirect(url_for('admin.ver_menu'))

@admin_bp.route("/admin/menu/editar/<int:id_plato>", methods=["GET"])
@requiere_login()
def editar_plato_vista(id_plato):
    """Muestra el formulario real con los datos corregidos."""
    CORRECT_BACKEND_URL = "http://127.0.0.1:5000/api"
    
    response = requests.get(f"{CORRECT_BACKEND_URL}/admin/menu/{id_plato}")
    
    if response.status_code == 200:
        plato = response.json()
        # 🚀 Volvemos a activar la plantilla real:
        return render_template('gestion/editar_plato.html', plato=plato)
    
    flash("No se pudo obtener el plato.", "danger")
    return redirect(url_for('admin.ver_menu'))

@admin_bp.route("/admin/menu/editar/<int:id_plato>/procesar", methods=["POST"])
@requiere_login()
def editar_plato_proceso(id_plato):
    """Recibe el formulario del Front (POST) y le manda un PATCH al Backend."""
    try:
        filename = None
        file = request.files.get("imagen")
        
        # Guardamos la imagen localmente si se subió una nueva
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(current_app.root_path, 'static', 'img')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            file.save(os.path.join(upload_folder, filename))

        # 🚀 ASEGURAMOS LOS TIPOS DE DATOS EXACTOS QUE TU BACKEND ESPERA
        payload = {
            "nombre_plato": str(request.form.get("nombre_plato", "")).strip(),
            "descripcion": str(request.form.get("descripcion", "")).strip(),
            "precio": float(request.form.get("precio", 0.0)),
            "estado": int(request.form.get("estado", 1)) # <-- Obligatorio que sea Entero (0 o 1)
        }

        # Si el usuario subió una foto nueva, la agregamos al paquete
        if filename:
            payload["imagen"] = filename

        # Conexión por PATCH a tu API del Backend
        url_backend = f"http://127.0.0.1:5000/api/admin/menu/{id_plato}"
        
        print(f"--- DATOS QUE ENVIAMOS AL BACKEND: {payload} ---")
        response = requests.patch(url_backend, json=payload)
        
        print(f"--- STATUS BACKEND AL GUARDAR: {response.status_code} ---")
        print(f"--- RESPUESTA DEL BACKEND: {response.text} ---")
        
        if response.status_code == 200:
            flash('¡Plato actualizado con éxito!', 'success')
        else:
            try:
                mensaje_error = response.json().get("mensaje", "Error desconocido")
            except:
                mensaje_error = response.text
            flash(f'El backend rechazó los cambios: {mensaje_error}', 'danger')
            
    except Exception as e:
        print(f"--- ERROR CRÍTICO AL GUARDAR: {e} ---")
        flash(f'Error de conexión: {e}', 'danger')
        
    return redirect(url_for('admin.ver_menu'))

@admin_bp.route("/admin/menu/eliminar/<int:id_plato>", methods=["POST"])
@requiere_login()
def eliminar_plato(id_plato):
    """Le avisa al Backend que tiene que eliminar el plato."""
    try:
        # 🚀 LE MANDAMOS UN DELETE AL BACKEND
        response = requests.delete(f"http://127.0.0.1:5000/api/admin/menu/{id_plato}")
        
        if response.status_code == 200:
            flash('Plato eliminado correctamente.', 'success')
        else:
            flash('No se pudo eliminar el plato en el servidor.', 'danger')
            
    except Exception as e:
        flash(f'Error al conectar con el servidor: {e}', 'danger')
        
    return redirect(url_for('admin.ver_menu'))

@admin_bp.route('/admin/dashboard/servicios')
@requiere_login()
def ver_servicios():
    try:
        response = requests.get(f"{BACKEND_URL}/servicios/")
        servicios = response.json() if response.status_code == 200 else []
    except Exception:
        servicios = []
    return render_template('gestion/servicios.html', servicios=servicios)


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