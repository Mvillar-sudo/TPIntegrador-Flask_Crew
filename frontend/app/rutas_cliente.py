from flask import Blueprint, render_template, request, redirect, url_for
import requests
# from backend.app.routes.reservas import reservas_bp
# from backend.app.routes.reseñas import reseñas_bp
# from backend.app.services.admin_menu_service import obtener_menu_admin_service
# from backend.app.services.servicios_service import (obtener_servicios)
# from backend.app.services.resenas_service import obtener_resenas
#
cliente_bp = Blueprint('cliente', __name__)

cliente_bp.register_blueprint(reservas_bp)
cliente_bp.register_blueprint(reseñas_bp)

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

    return render_template('menu.html', platos=platos_activos)