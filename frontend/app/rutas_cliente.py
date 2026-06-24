from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
import requests
import os

cliente_bp = Blueprint('cliente', __name__)

BACKEND_URL = "http://localhost:5000"

cliente_bp = Blueprint('cliente', __name__)


@cliente_bp.route('/', methods=['GET'])
def landing():
    try:
        response = requests.get(f"{BACKEND_URL}/api/servicios/", timeout=3)
        servicios = response.json() if response.status_code == 200 else []
    except Exception as e:
        flash(f'Error al conectar la API con sericios: {e}', 'danger')
        servicios = []
        
    return render_template('landing.html', servicios=servicios)



@cliente_bp.route('/menu', methods=['GET'])
def menu():
    try:
        response = requests.get(f"{BACKEND_URL}/menu")
        platos_activos = response.json() if response.status_code == 200 else []
        platos_activos = response.json() if response.status_code == 200 else []
        
        ruta_static_img = os.path.join(current_app.root_path, 'static', 'img')

        for plato in platos_activos:
            if plato.get("precio") is not None:
                try:
                    plato["precio"] = float(plato["precio"])
                except (ValueError, TypeError):
                    plato["precio"] = 0.00
            else:
                plato["precio"] = 0.00
            nombre_imagen = plato.get("imagen")
            if nombre_imagen:
                ruta_fisica_imagen = os.path.join(ruta_static_img, nombre_imagen)
                
                # Si el archivo NO existe físicamente, se cambia a None para usar la default
                if not os.path.exists(ruta_fisica_imagen):
                    plato["imagen"] = None


    except Exception:
        platos_activos = []
    return render_template('menu.html', platos=platos_activos)


def obtener_resenas_backend():
    """Función auxiliar para conectarse a la API del backend."""
    try:
        respuesta = requests.get(f"{BACKEND_URL}/api/resenas/", timeout=10)
        if respuesta.status_code == 200:
            return respuesta.json()
    except Exception as e:
       flash(f'Error al conectar al backend de reseñas: {e}', 'danger') 
    return []


@cliente_bp.route('/resenas', methods=['GET'])
def resenas():
    """Muestra la página de opiniones y lista todas las reseñas existentes."""
    exito = request.args.get('exito') == 'True'
    error = request.args.get('error')

    try:
        respuesta = requests.get(f"{BACKEND_URL}/api/resenas/", timeout=10)
        resenas_list = respuesta.json() if respuesta.status_code == 200 else []
    except Exception:
        resenas_list = []
    
    return render_template('resenas.html', resenas=resenas_list, exito=exito, error=error)


@cliente_bp.route('/resenas/crear', methods=['POST'])
def crear_resena():
    """Recibe el formulario clásico HTML de reseña y lo envía al backend."""
    nombre_cliente = request.form.get('nombre_cliente', '').strip()
    email          = request.form.get('email', '').strip()
    calificacion   = request.form.get('calificacion', '').strip()
    comentario     = request.form.get('comentario', '').strip()

    payload = {
        "nombre_cliente": nombre_cliente,
        "email": email,
        "calificacion": int(calificacion) if calificacion.isdigit() else None,
        "comentario": comentario
    }

    try:
        respuesta = requests.post(f"{BACKEND_URL}/api/resenas/", json=payload, timeout=10)

        if respuesta.status_code == 201:
            return redirect(url_for('cliente.resenas', exito='True'))
        else:
            msg_error = respuesta.json().get('error', 'No se pudo procesar la reseña.')
            return redirect(url_for('cliente.resenas', error=msg_error))

    except Exception:
        return redirect(url_for('cliente.resenas', error='No se pudo conectar con el servidor central.'))

@cliente_bp.route('/reservas/nueva', methods=['POST'])
def crear_reserva():
    data = {
        "nombre": request.form.get("name"),
        "email": request.form.get("Email"),
        "fecha": request.form.get("fecha"),
        "hora": request.form.get("hora"),
        "cantidad_personas": request.form.get("persons"),
        "telefono": "0000000000"  # el form no tiene campo telefono
    }
    
    try:
        r = requests.post(f"{BACKEND_URL}/api/reservas/", json=data)
        if r.status_code == 201:
            flash('¡Una reserva ha sido creada con éxito!', 'reservas')
            return redirect(url_for('cliente.landing'))
        else:
            error = r.json().get("mensaje", "Error al crear la reserva")
            return render_template('landing.html', error=error)
    except Exception as e:
        flash(f'Error al crear reserva: {e}', 'danger')
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
        flash(f'Error al cancelar reserva: {e}', 'danger')
        return render_template('cancelacion.html', exito=False, mensaje="Error de conexión con el servidor")