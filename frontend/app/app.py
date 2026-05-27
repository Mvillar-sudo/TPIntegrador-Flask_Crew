from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_hamburgueseria'

@app.route('/', methods=['GET', 'POST'])
def landing():
    """
    Página Principal. 
    Mapea 'landing' (como pide base.html) pero renderiza 'landing.html'.
    Procesa reservas rápidas y suscripciones.
    """
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
            
        return redirect(url_for('landing'))
        
    return render_template('landing.html')


@app.route('/menu')
def menu():
    """
    Menú de Platos.
    Envía los datos dinámicos a 'menu.html' para evitar repetir código.
    """
    platos_hamburgueseria = [
        {"nombre": "Fresh Mushrooms", "descripcion": "Far far away, behind the word...", "precio": 19.15, "imagen": "img_2.jpg"},
        {"nombre": "Cheese and Garlic Toast", "descripcion": "Far far away, behind the word...", "precio": 20.99, "imagen": "img_3.jpg"},
        {"nombre": "Grilled Chicken Salad", "descripcion": "Far far away, behind the word...", "precio": 8.99, "imagen": "img_4.jpg"},
        {"nombre": "Organic Egg", "descripcion": "Far far away, behind the word...", "precio": 12.99, "imagen": "img_5.jpg"},
        {"nombre": "Tomato Soup with Chicken", "descripcion": "Far far away, behind the word...", "precio": 23.10, "imagen": "img_6.jpg"},
        {"nombre": "Salad with Crispy Chicken", "descripcion": "Far far away, behind the word...", "precio": 5.59, "imagen": "img_7.jpg"}
    ]
    return render_template('menu.html', platos=platos_hamburgueseria)


@app.route('/reservas', methods=['GET', 'POST'])
def reservas():
    """
    Página independiente de Reservas.
    """
    if request.method == 'POST':
        return redirect(url_for('landing'))
    return render_template('reservas.html')


@app.route('/resenas', methods=['GET', 'POST'])
def resenas():
    """
    Página de Reseñas (resenas.html).
    Muestra el formulario (GET) y procesa la opinión enviada (POST).
    """
    if request.method == 'POST':
        nombre = request.form.get('name')
        email = request.form.get('email')
        calificacion = request.form.get('rating') 
        opinion = request.form.get('opinion')
        
        print(f"[Nueva Reseña] {nombre} ({email}) le dio {calificacion} estrellas.")
        print(f"Comentario: {opinion}")
        
        return redirect(url_for('resenas'))
        
    return render_template('resenas.html')


if __name__ == '__main__':
    app.run(port = 3000, debug=True)