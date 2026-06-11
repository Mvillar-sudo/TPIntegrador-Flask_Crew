import requests
from flask import Blueprint, render_template, request, redirect, url_for
from backend.app.routes.resena import resenas_bp
from backend.app.services.admin_menu_service import obtener_menu_admin_service
from backend.app.services.servicios_service import (obtener_servicios)
from backend.app.services.resenas_service import obtener_resenas
BACKEND_URL = "http://localhost:5000"

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/', methods=['GET', 'POST'])
def landing():
    if request.method == 'POST':
        if 'email' in request.form and 'persons' not in request.form:
            # Formulario de suscripción
            email = request.form.get('email')
            print(f"[Newsletter] Nuevo suscriptor: {email}")
        else:
            # Formulario de reserva rápida del Header
            personas = request.form.get('persons')
            fecha = request.form.get('date')
            hora = request.form.get('time')
            print(f"[Reserva Rápida] {personas} personas para el {fecha} a las {hora}")
            
        return redirect(url_for('cliente.landing'))
        
    try:
        servicios = obtener_servicios()
        return render_template('landing.html', servicios=servicios)
    except RuntimeError as e:
        return "No se encontro el abm", 500 

@cliente_bp.route('/menu')
def menu():
    try:
        platos = obtener_menu_admin_service()

        return render_template('menu.html', platos=platos)
    except Exception as e:
        print(f"Error crítico en /admin/menu: {e}")
        return f"Error interno del servidor: {e}", 500
    

@cliente_bp.route('/dejar-resena', methods=['GET'])
def pagina_resenas():
    try:
        todas_las_resenas = obtener_resenas()
        
        ultimas_resenas = todas_las_resenas[:6] 
    except Exception:
        ultimas_resenas = []

    return render_template('resenas.html', resenas=ultimas_resenas)

@cliente_bp.route('/menu', methods=['GET'])
def ver_menu_publico():
    try:
        response = requests.get("http://127.0.0.1:5000/menu")

        platos = []
        if response.status_code == 200:
            platos = response.json()
        else:
            print(f"Advertencia: El Backend devolvió código {response.status_code}")

        return render_template('menu.html', platos=platos)
    except Exception as e:
        print(f"Error crítico en /admin/menu: {e}")
        return f"Error interno del servidor: {e}", 500

@cliente_bp.route('/reservas/nueva', methods=['POST'])
def crear_reserva():
    data = {
        "nombre": request.form.get("name"),
        "email": request.form.get("Email"),
        "fecha": request.form.get("fecha"),
        "hora": request.form.get("hora"),
        "cantidad_personas": request.form.get("persons"),
        "telefono": ""  # el form no tiene campo telefono
    }

    try:
        r = requests.post(f"{BACKEND_URL}/api/reservas/", json=data)
        if r.status_code == 201:
            return redirect(url_for('cliente.landing'))
        else:
            error = r.json().get("mensaje", "Error al crear la reserva")
            return render_template('landing.html', error=error)
    except Exception as e:
        print(f"Error al crear reserva: {e}")
        return render_template('landing.html', error="Error de conexión con el servidor")


@cliente_bp.route('/reservas/cancelar/<string:token>', methods=['GET'])
def cancelar_reserva(token):
    try:
        r = requests.get(f"{BACKEND_URL}/api/reservas/cancelar/{token}")
        mensaje = r.json().get("mensaje", "")
        if r.status_code == 200:
            return render_template('cancelacion.html', exito=True, mensaje=mensaje)
        else:
            return render_template('cancelacion.html', exito=False, mensaje=mensaje)
    except Exception as e:
        print(f"Error al cancelar reserva: {e}")
        return render_template('cancelacion.html', exito=False, mensaje="Error de conexión con el servidor")



