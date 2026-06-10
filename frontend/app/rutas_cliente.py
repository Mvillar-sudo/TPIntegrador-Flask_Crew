from flask import Blueprint, render_template, request, redirect, url_for
import requests

cliente_bp = Blueprint('cliente', __name__)

BACKEND_RESENAS_URL = 'http://localhost:5000/api/resenas/'

def obtener_resenas_backend():
    respuesta = requests.get(BACKEND_RESENAS_URL, timeout=10)
    respuesta.raise_for_status()
    return respuesta.json()

def render_resenas(exito, error):
    try:
        resenas_list = obtener_resenas_backend()
    except Exception:
        resenas_list = []
    return render_template('resenas.html', resenas=resenas_list, exito=exito, error=error)

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

@cliente_bp.route('/')
def index():
    lista_servicios = get_servicio() 
    
    return render_template('index.html', servicios=lista_servicios)

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

@cliente_bp.route('/resenas', methods=['GET', 'POST'])
def resenas():
    if request.method == 'POST':
        nombre_cliente = request.form.get('nombre_cliente', '').strip()
        calificacion   = request.form.get('calificacion', '').strip()
        comentario     = request.form.get('comentario', '').strip()
        reserva_id     = request.form.get('reserva_id', '').strip()

        payload = {
            "nombre_cliente": nombre_cliente,
            "calificacion": int(calificacion) if calificacion else None,
            "comentario": comentario,
            "reserva_id": int(reserva_id) if reserva_id else None,
        }

        try:
            respuesta = requests.post(BACKEND_RESENAS_URL, json=payload, timeout=10)
            if respuesta.status_code != 201:
                error = respuesta.json().get('error', 'No se pudo crear la reseña')
                return render_resenas(exito=False, error=error)
        except Exception:
            return render_resenas(exito=False, error='No se pudo conectar con el servidor')

        return render_resenas(exito=True, error=None)

    return render_resenas(exito=False, error=None)