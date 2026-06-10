import requests
from flask import Blueprint, render_template, request, redirect, url_for
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
        
    return render_template('landing.html')


@cliente_bp.route('/menu')
def menu():
    platos_hamburgueseria = [
        {"nombre": "Fresh Mushrooms", "descripcion": "Far far away, behind the word...", "precio": 19.15, "imagen": "img_2.jpg"},
        {"nombre": "Cheese and Garlic Toast", "descripcion": "Far far away, behind the word...", "precio": 20.99, "imagen": "img_3.jpg"},
        {"nombre": "Grilled Chicken Salad", "descripcion": "Far far away, behind the word...", "precio": 8.99, "imagen": "img_4.jpg"},
        {"nombre": "Organic Egg", "descripcion": "Far far away, behind the word...", "precio": 12.99, "imagen": "img_5.jpg"},
        {"nombre": "Tomato Soup with Chicken", "descripcion": "Far far away, behind the word...", "precio": 23.10, "imagen": "img_6.jpg"},
        {"nombre": "Salad with Crispy Chicken", "descripcion": "Far far away, behind the word...", "precio": 5.59, "imagen": "img_7.jpg"}
    ]
    return render_template('menu.html', platos=platos_hamburgueseria)


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
    
    
    
