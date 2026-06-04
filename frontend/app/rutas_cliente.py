from flask import Blueprint, render_template, request, redirect, url_for
from backend.app.routes.reservas import reservas_bp

cliente_bp = Blueprint('cliente', __name__)

cliente_bp.register_blueprint(reservas_bp)

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