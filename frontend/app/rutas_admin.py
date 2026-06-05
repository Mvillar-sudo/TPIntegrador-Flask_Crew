from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from backend.app.routes.auth import auth_bp
from backend.app.routes.admin_menu import admin_menu_bp
from backend.app.services.admin_menu_service import (obtener_menu_admin_service, obtener_plato_service, cambiar_estado_plato_service, actualizar_parcial_plato_service, eliminar_plato_service, crear_plato_service)
from backend.app.db import query_db, execute_db

admin_bp = Blueprint('admin', __name__)

admin_bp.register_blueprint(auth_bp)
admin_bp.register_blueprint(admin_menu_bp)

@admin_bp.route('/admin/login')
def login():
    return render_template('gestion/login.html')

@admin_bp.route('/admin/login_process', methods=['POST'])
def login_process():
    usuario = request.form.get('username')
    contrasena = request.form.get('password')
    
    if usuario == "admin" and contrasena == "123":
        session['admin_logeado'] = True
        return redirect(url_for('admin.dashboard')) 

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
def servicios():
    if not session.get('admin_logeado'): 
        return redirect(url_for('admin.login'))
        
    servicios_lista = [
        {"id": 1, "nombre": "Catering Eventos", "activo": True, "fecha_creacion": "2026-03-01"},
        {"id": 2, "nombre": "Delivery VIP", "activo": False, "fecha_creacion": "2026-04-10"}
    ]
    return render_template('gestion/servicios.html', servicios=servicios_lista)