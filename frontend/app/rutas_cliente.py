import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash

cliente_bp = Blueprint('cliente', __name__)

BACKEND_URL = "http://localhost:5000/api"

@cliente_bp.route('/', methods=['GET'])
def landing():
    try:
        response = requests.get(f"{BACKEND_URL}/servicios/")
        servicios = response.json() if response.status_code == 200 else []
    except Exception:
        servicios = []
    return render_template('landing.html', servicios=servicios)


@cliente_bp.route('/menu', methods=['GET'])
def menu():
    try:
        response = requests.get(f"{BACKEND_URL}/menu")
        platos_activos = response.json() if response.status_code == 200 else []
    except Exception:
        platos_activos = []
    return render_template('menu.html', platos=platos_activos)


@cliente_bp.route('/dejar-resena', methods=['GET'])
def dejar_resena():
    try:
        response = requests.get(f"{BACKEND_URL}/resenas/")
        if response.status_code == 200:
            todas_las_resenas = response.json()
            ultimas_resenas = todas_las_resenas[:6] 
        else:
            ultimas_resenas = []
    except Exception:
        ultimas_resenas = []
    return render_template('resenas.html', resenas=ultimas_resenas)


@cliente_bp.route('/dejar-resena/proceso', methods=['POST'])
def procesar_nueva_resena():
    payload = {
        "nombre_cliente": request.form.get("nombre", "").strip(),
        "comentario": request.form.get("comentario", "").strip(),
        "calificacion": int(request.form.get("puntuacion", 5))
    }
    try:
        response = requests.post(f"{BACKEND_URL}/resenas/", json=payload)
        if response.status_code == 201:
            flash("¡Gracias por tu opinión!", "success")
        else:
            flash("No se pudo guardar la reseña.", "danger")
    except Exception:
        flash("Error de conexión con el servidor.", "danger")
    return redirect(url_for('cliente.dejar_resena'))


@cliente_bp.route('/reservar_proceso', methods=['POST'])
def procesar_reserva_cliente():
    payload = {
        "nombre": request.form.get("nombre"),
        "email": request.form.get("email"),
        "telefono": request.form.get("telefono"),
        "fecha": request.form.get("date"),       
        "hora": request.form.get("time"),         
        "cantidad_personas": int(request.form.get("persons", 1))
    }
    try:
        response = requests.post(f"{BACKEND_URL}/reservas/", json=payload)
        if response.status_code == 201:
            flash("¡Reserva creada con éxito!", "success")
        else:
            mensaje = response.json().get("mensaje", "No hay disponibilidad.")
            flash(mensaje, "danger")
    except Exception:
        flash("Error con el servidor de reservas.", "danger")
    return redirect(url_for('cliente.landing'))


@cliente_bp.route('/cancelar-reserva/<string:token>', methods=['GET'])
def cancelar_via_email(token):
    try:
        response = requests.get(f"{BACKEND_URL}/reservas/cancelar/{token}")
        if response.status_code == 200:
            return "<h1>Reserva cancelada correctamente.</h1>"
        else:
            return f"<h1>Error: {response.json().get('mensaje')}</h1>", 400
    except Exception:
        return "<h1>Error de conexión.</h1>", 500