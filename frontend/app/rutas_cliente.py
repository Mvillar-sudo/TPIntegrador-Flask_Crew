from flask import Blueprint, render_template, request, redirect, url_for
from backend.app.routes.reservas import reservas_bp
from backend.app.routes.reseñas import reseñas_bp
from backend.app.services.admin_menu_service import obtener_menu_admin_service
from backend.app.services.servicios_service import obtener_servicios

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
    

@cliente_bp.route('/reservas', methods=['GET', 'POST'])
def reservas():
    if request.method == 'POST':
        return redirect(url_for('cliente.landing'))
    return render_template('reservas.html')


@cliente_bp.route('/resenas', methods=['GET', 'POST'])
def resenas():
    if request.method == 'POST':
        nombre = request.form.get('name')
        email = request.form.get('email')
        calificacion = request.form.get('rating') 
        opinion = request.form.get('opinion')
        
        print(f"[Nueva Reseña] {nombre} ({email}) le dio {calificacion} estrellas.")
        print(f"Comentario: {opinion}")
        
        return redirect(url_for('cliente.resenas'))
        
    return render_template('resenas.html')