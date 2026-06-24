import requests
import os
import datetime
from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash, current_app, session
from werkzeug.utils import secure_filename

from utils import requiere_login, guardar_sesion, limpiar_sesion, extraer_mensajes_error

admin_bp = Blueprint('admin', __name__)

BACKEND_URL = "http://localhost:5000/api"

@admin_bp.route('/admin/login', methods=['GET'])
def login():
    return render_template('gestion/login.html')


@admin_bp.route('/admin/login_process', methods=['POST'])
def login_process():
    payload = {
        "email": request.form.get('username'),
        "password": request.form.get('password')
    }
    try:
        response = requests.post(f"{BACKEND_URL}/login", json=payload)
        res_data = response.json()

        if response.status_code == 200:
            guardar_sesion(res_data.get("token"), {"nombre": res_data.get("usuario")})
            flash("¡Bienvenido al panel!", "success")
            return redirect(url_for('admin.dashboard'))
        else:
            errores = extraer_mensajes_error(res_data)
            flash(errores[0], "danger")
            return redirect(url_for('admin.login'))
    except Exception:
        flash("Error: No se pudo conectar con el servidor de autenticación.", "danger")
        return redirect(url_for('admin.login'))


@admin_bp.route('/admin/logout')
def logout():
    limpiar_sesion()
    flash("Sesión cerrada.", "info")
    return redirect(url_for('admin.login'))

@admin_bp.route("/admin/registrar", methods=["GET"])
@requiere_login()
def mostrar_formulario_crear():
    try:
        return render_template('gestion/registrar.html')
        
    except Exception as e:
        flash(f'Error al cargar la página: {e}', 'danger')
        return redirect(url_for('admin.dashboard')) 

@admin_bp.route("/admin/registrar_usuario_proceso", methods=["POST"])
@requiere_login()
def registrar_usuario_proceso():
    try:
        payload = {
            "nombre": request.form.get("nombre", "").strip(),
            "email": request.form.get("email", "").strip(),
            "password": request.form.get("password", "").strip()
        }

        response = requests.post(f"{BACKEND_URL}/register", json=payload)
        
        if response.status_code == 201:
            flash('¡Administrador añadido exitosamente!', 'success')
            return redirect(url_for('admin.ver_usuarios')) 
        else:
            error_mensaje = response.json().get("mensaje", "Error al crear el usuario")
            flash(error_mensaje, 'danger')
            
    except Exception as e:
        flash(f'Error al procesar el registro: {e}', 'danger')
        
    return redirect(url_for('admin.mostrar_formulario_crear'))

@admin_bp.route('/admin/dashboard/usuarios')
@requiere_login()
def ver_usuarios():
    try:
        response = requests.get(f"{BACKEND_URL}/admin/usuarios")
        usuarios = response.json() if response.status_code == 200 else []
    except Exception:
        usuarios = []
    return render_template('gestion/usuarios.html', usuarios=usuarios)


@admin_bp.route('/admin/usuarios/editar/<int:id_usuario>', methods=['GET', 'POST'])
@requiere_login() 
def editar_usuario_vista(id_usuario):
    if request.method == 'POST':
        data_formulario = {
            "nombre": request.form.get("nombre"),
            "email": request.form.get("email"),
            "password": request.form.get("password"),
            "activo": int(request.form.get("activo", 0))
        }
        
        try:
            response = requests.patch(f"{BACKEND_URL}/admin/usuarios/{id_usuario}", json=data_formulario, timeout=3)
            
            if response.status_code == 200:
                flash("Usuario actualizado correctamente.", "success")
                return redirect(url_for('admin.ver_usuarios'))
            else:
                error_api = response.json().get("error", "Error al actualizar")
                flash(f"Error: {error_api}", "danger")
        except requests.exceptions.RequestException:
            flash("Error de conexión con el servidor de datos.", "danger")

    try:
        response = requests.get(f"{BACKEND_URL}/admin/usuarios/{id_usuario}", timeout=3)
        if response.status_code == 200:
            usuario = response.json()
            return render_template('gestion/editar_usuario.html', usuario=usuario)
        else:
            flash("No se pudo encontrar el usuario solicitado.", "danger")
            return redirect(url_for('admin.ver_usuarios'))
            
    except requests.exceptions.RequestException:
        flash("Error al conectar con el servidor.", "danger")
        return redirect(url_for('admin.ver_usuarios'))

@admin_bp.route('/admin/usuarios/eliminar/<int:id_usuario>', methods=['POST'])
def eliminar_usuario_vista(id_usuario):
    try:
        response = requests.delete(f"{BACKEND_URL}/admin/usuarios/{id_usuario}", timeout=3)
        if response.status_code == 200:
            flash("Usuario eliminado correctamente.", "success")
        else:
            flash("No se pudo eliminar el servicio.", "danger")
    except requests.exceptions.RequestException:
        flash("Error de conexión con el backend.", "danger")
        
    return redirect(url_for('admin.ver_usuarios'))

@admin_bp.route('/admin/dashboard')
@requiere_login()
def dashboard():
    total_platos = 0
    total_reservas = 0
    total_servicios = 0
    total_resenas_positivas = 0
    total_resenas_negativas = 0
    total_usuarios = 0
    try:
        response = requests.get(f"{BACKEND_URL}/dashboard/metricas")
        if response.status_code == 200:
            metricas = response.json().get("data", {})
            total_platos = metricas.get("total_platos_activos", 0)
            total_reservas = metricas.get("total_reservas_pendientes", 0)
            total_servicios = metricas.get("total_servicios_activos", 0)
            total_resenas_positivas = metricas.get("total_resenas_positivas", 0)
            total_resenas_negativas = metricas.get("total_resenas_negativas", 0)
            total_usuarios = metricas.get("total_usuarios", 0)
    except requests.exceptions.RequestException as e:
        flash(f'Error de red: {e}', 'danger')

    return render_template(
        'gestion/dashboard.html', 
        total_platos=total_platos, 
        total_reservas=total_reservas, 
        total_servicios=total_servicios,
        total_resenas_positivas=total_resenas_positivas,
        total_resenas_negativas=total_resenas_negativas,
        total_usuarios = total_usuarios
    ) 

@admin_bp.route('/admin/api/metricas-en-vivo')
@requiere_login() 
def metricas_en_vivo():
    try:
        response = requests.get(f"{BACKEND_URL}/dashboard/metricas")
        if response.status_code == 200:
            metricas = response.json().get("data", {})
            
            p = metricas.get("total_platos_activos", 0)
            r = metricas.get("total_reservas_pendientes", 0)
            s = metricas.get("total_servicios_activos", 0)
            rp = metricas.get("total_resenas_positivas", 0)  
            rn = metricas.get("total_resenas_negativas", 0)  
            u = metricas.get("total_usuarios", 0)
            
            hora_actual = datetime.datetime.now().strftime("%H:%M:%S")

           
            estructura_base = {
                "platos": [], 
                "reservas": [], 
                "servicios": [], 
                "resenas_positivas": [], 
                "resenas_negativas": [], 
                "usuarios": [],          
                "tiempos": []
            }
            historial = session.get('grafico_historial', estructura_base)
            
            
            for clave in ["resenas_positivas", "resenas_negativas", "usuarios"]:
                if clave not in historial or not isinstance(historial[clave], list):
                    historial[clave] = [0] * len(historial.get("tiempos", []))

            
            historial["platos"].append(p)
            historial["reservas"].append(r)
            historial["servicios"].append(s)
            historial["resenas_positivas"].append(rp) 
            historial["resenas_negativas"].append(rn) 
            historial["usuarios"].append(u)           
            historial["tiempos"].append(hora_actual)

            # Mantener solo los últimos 12 registros de forma segura y dinámica
            if len(historial["tiempos"]) > 12:
                for lista in historial.values():
                    if isinstance(lista, list) and len(lista) > 0:
                        lista.pop(0)

            session['grafico_historial'] = historial 
            session.modified = True 
            
            
            return jsonify({
                "actual": {
                    "platos": p, 
                    "reservas": r, 
                    "servicios": s,
                    "resenas_positivas": rp, 
                    "resenas_negativas": rn, 
                    "usuarios": u            
                },
                "historial": historial
            })
            
    except requests.exceptions.RequestException as e:
        flash(f'Error de red: {e}', 'danger')
    
    return jsonify({"error": "No se pudieron obtener datos"}), 500

@admin_bp.route("/admin/menu", methods=["GET"])
@requiere_login()
def ver_menu():
    try:
        
        response = requests.get(f"{BACKEND_URL}/admin/menu")

        if response.status_code == 200:
            platos = response.json() 
        else:
            platos = []
            
        upload_folder = os.path.join(current_app.root_path, 'static', 'img')

        if platos:
            for plato in platos:
                imagen_nombre = plato.get("imagen")
                
                if imagen_nombre:
                    ruta_fisica = os.path.join(upload_folder, imagen_nombre)
                    
                    # ¡SI LA IMAGEN FUE BORRADA DEL DISCO!
                    if not os.path.exists(ruta_fisica):
                        
    
                        id_plato = plato.get("id_plato")
                        payload_limpieza = {
                            "nombre_plato": plato.get("nombre_plato"),
                            "descripcion": plato.get("descripcion"),
                            "precio": plato.get("precio"),
                            "estado": plato.get("estado"),
                            "imagen": None  
                        }
                        
                        requests.patch(f"{BACKEND_URL}/admin/menu/{id_plato}", json=payload_limpieza)
                        
                        plato["imagen"] = None

    except Exception as e:
        platos = []
        
    return render_template('gestion/menu.html', platos=platos)

@admin_bp.route("/admin/menu/crear", methods=["GET"])
def crear_plato_vista():
    return render_template('gestion/crear_plato.html')

@admin_bp.route("/admin/menu/crear_proceso", methods=["POST"])
@requiere_login()
def crear_plato_proceso():
    try:
        filename = None
        file = request.files.get("imagen")
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(current_app.root_path, 'static', 'img')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            

        payload = {
            "nombre_plato": request.form.get("nombre_plato", "").strip(),
            "descripcion": request.form.get("descripcion", "").strip(),
            "imagen": filename,
            "precio": float(request.form.get("precio", 0))
        }

        response = requests.post(f"{BACKEND_URL}/admin/menu", json=payload)
        if response.status_code == 201:
            flash('¡Plato añadido exitosamente!', 'success')
            file.save(os.path.join(upload_folder, filename))
        else:
            flash(response.json().get("mensaje", "Error al crear"), 'danger')
    except Exception as e:
        flash(f'Error al procesar: {e}', 'danger')
    return redirect(url_for('admin.ver_menu'))

@admin_bp.route("/admin/menu/editar/<int:id_plato>", methods=["GET"])
@requiere_login()
def editar_plato_vista(id_plato):
    
    response = requests.get(f"{BACKEND_URL}/admin/menu/{id_plato}")
    
    if response.status_code == 200:
        plato = response.json()
        imagen_nombre = plato.get("imagen")
        
        if imagen_nombre:
            upload_folder = os.path.join(current_app.root_path, 'static', 'img')
            ruta_fisica = os.path.join(upload_folder, imagen_nombre)
            
            # ¡SI LA IMAGEN FUE BORRADA FÍSICAMENTE!
            if not os.path.exists(ruta_fisica):
                
                payload_limpieza = {
                    "nombre_plato": plato.get("nombre_plato"),
                    "descripcion": plato.get("descripcion"),
                    "precio": plato.get("precio"),
                    "estado": plato.get("estado"),
                    "imagen": None 
                }
                requests.patch(f"{BACKEND_URL}/admin/menu/{id_plato}", json=payload_limpieza)
                

                plato["imagen"] = None
        
        return render_template('gestion/editar_plato.html', plato=plato)
    
    flash("No se pudo obtener el plato.", "danger")
    return redirect(url_for('admin.ver_menu'))

@admin_bp.route("/admin/menu/editar/<int:id_plato>/procesar", methods=["POST"])
@requiere_login()
def editar_plato_proceso(id_plato):
    try:
        filename = None
        file = request.files.get("imagen")
        
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(current_app.root_path, 'static', 'img')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            file.save(os.path.join(upload_folder, filename))

        payload = {
            "nombre_plato": str(request.form.get("nombre_plato", "")).strip(),
            "descripcion": str(request.form.get("descripcion", "")).strip(),
            "precio": float(request.form.get("precio", 0.0)),
            "estado": int(request.form.get("estado", 1)) 
        }

       
        if filename:
            payload["imagen"] = filename

       
        url_backend = f"{BACKEND_URL}/admin/menu/{id_plato}"
        
        response = requests.patch(url_backend, json=payload)
        
        
        if response.status_code == 200:
            flash('¡Plato actualizado con éxito!', 'success')
        else:
            try:
                mensaje_error = response.json().get("mensaje", "Error desconocido")
            except:
                mensaje_error = response.text
            flash(f'El backend rechazó los cambios: {mensaje_error}', 'danger')
            
    except Exception as e:
        flash(f'Error de conexión: {e}', 'danger')
        
    return redirect(url_for('admin.ver_menu'))

@admin_bp.route("/admin/menu/eliminar/<int:id_plato>", methods=["POST"])
@requiere_login()
def eliminar_plato(id_plato):
    """Le avisa al Backend que tiene que eliminar el plato."""
    try:
       
        response = requests.delete(f"{BACKEND_URL}/admin/menu/{id_plato}")
        
        if response.status_code == 200:
            flash('Plato eliminado correctamente.', 'success')
        else:
            flash('No se pudo eliminar el plato en el servidor.', 'danger')
            
    except Exception as e:
        flash(f'Error al conectar con el servidor: {e}', 'danger')
        
    return redirect(url_for('admin.ver_menu'))

@admin_bp.route('/admin/dashboard/servicios')
@requiere_login()
def ver_servicios():
    try:
        response = requests.get(f"{BACKEND_URL}/servicios/")
        servicios = response.json() if response.status_code == 200 else []
    except Exception:
        servicios = []
    return render_template('gestion/servicios.html', servicios=servicios)


@admin_bp.route('/admin/servicios/nuevo', methods=['GET', 'POST'])
def crear_servicio_vista():
    if request.method == 'POST':
        data_formulario = {
            "nombre": request.form.get("nombre")
        }
        
        try:
            response = requests.post(f"{BACKEND_URL}/servicios/", json=data_formulario, timeout=3)
            
            if response.status_code == 201:
                flash("¡Servicio creado con éxito!", "success")
                return redirect(url_for('admin.ver_servicios'))  
            else:
                error_api = response.json().get("error", "Error desconocido")
                flash(f"No se pudo crear: {error_api}", "danger")
                
        except requests.exceptions.RequestException as e:
            flash("Error de conexión con el servidor de datos.", "danger")

    return render_template('gestion/crear_servicio.html')


@admin_bp.route('/admin/servicios/eliminar/<int:id_servicio>', methods=['POST'])
def eliminar_servicio_vista(id_servicio):
    try:
        response = requests.delete(f"{BACKEND_URL}/servicios/{id_servicio}", timeout=3)
        if response.status_code == 200:
            flash("Servicio eliminado correctamente.", "success")
        else:
            flash("No se pudo eliminar el servicio.", "danger")
    except requests.exceptions.RequestException:
        flash("Error de conexión con el backend.", "danger")
        
    return redirect(url_for('admin.ver_servicios'))

@admin_bp.route('/admin/servicios/editar/<int:id_servicio>', methods=['GET', 'POST'])
@requiere_login() 
def editar_servicio_vista(id_servicio):
    if request.method == 'POST':
        data_formulario = {
            "nombre": request.form.get("nombre"),
            "activo": True if request.form.get("activo") else False
        }
        
        try:
            response = requests.patch(f"{BACKEND_URL}/servicios/{id_servicio}", json=data_formulario, timeout=3)
            
            if response.status_code == 200:
                flash("Servicio actualizado correctamente.", "success")
                return redirect(url_for('admin.ver_servicios'))
            else:
                error_api = response.json().get("error", "Error al actualizar")
                flash(f"Error: {error_api}", "danger")
        except requests.exceptions.RequestException:
            flash("Error de conexión con el servidor de datos.", "danger")

    try:
        response = requests.get(f"{BACKEND_URL}/servicios/{id_servicio}", timeout=3)
        if response.status_code == 200:
            servicio = response.json()
            return render_template('gestion/editar_servicio.html', servicio=servicio)
        else:
            flash("No se pudo encontrar el servicio solicitado.", "danger")
            return redirect(url_for('admin.ver_servicios'))
            
    except requests.exceptions.RequestException:
        flash("Error al conectar con el servidor.", "danger")
        return redirect(url_for('admin.ver_servicios'))

@admin_bp.route('/admin/dashboard/servicios/editar/<int:id_servicio>/procesar', methods=['POST'])
@requiere_login()
def actualizar_servicio_proceso(id_servicio):
    payload = {
        "nombre": request.form.get("nombre", "").strip(),
        "activo": (request.form.get("activo") == "True")  
    }
    try:
        response = requests.patch(f"{BACKEND_URL}/servicios/{id_servicio}", json=payload)
        if response.status_code == 200:
            flash('¡Servicio modificado!', 'success')
        else:
            flash(response.json().get("error", "Error"), "danger")
    except Exception:
        flash("Error al conectar con la API", "danger")
    return redirect(url_for('admin.ver_servicios'))

@admin_bp.route('/admin/dashboard/resenas')
@requiere_login()
def ver_resenas():
    try:
        response = requests.get(f"{BACKEND_URL}/resenas/")
        resenas = response.json() if response.status_code == 200 else []
    except Exception:
        resenas = []
    return render_template(
        'gestion/resenas.html',
        resenas=resenas,
        titulo_pagina='Reseñas de Clientes',
        subtitulo_pagina='Gestioná los comentarios dejados por los clientes'
    )


@admin_bp.route('/admin/resenas/eliminar/<int:id_resena>', methods=['POST'])
@requiere_login()
def eliminar_resena_vista(id_resena):
    try:
        response = requests.delete(f"{BACKEND_URL}/resenas/{id_resena}")
        if response.status_code == 200:
            flash("Reseña eliminada correctamente.", "success")
        else:
            flash("No se pudo eliminar la reseña.", "danger")
    except requests.exceptions.RequestException:
        flash("Error de conexión con el backend.", "danger")

    return redirect(url_for('admin.ver_resenas'))

@admin_bp.route('/admin/dashboard/reservas')
@requiere_login()
def reservas():
    try:
        r = requests.get(f"{BACKEND_URL}/reservas/")
        reservas_lista = r.json()
    except Exception as e:
        reservas_lista = []
    
    return render_template('gestion/reservas.html', reservas=reservas_lista)


@admin_bp.route('/admin/dashboard/reservas/<int:id_reserva>/cancelar', methods=['POST'])
@requiere_login()
def cancelar_reserva(id_reserva):
    try:
        r = requests.patch(f"{BACKEND_URL}/reservas/{id_reserva}/cancelar")
        flash(r.json().get("mensaje", ""), "success" if r.status_code == 200 else "danger")
    except Exception as e:
        flash("Error de conexión con el servidor", "danger")
    
    return redirect(url_for('admin.reservas'))

@admin_bp.route('/admin/dashboard/validar-qr', methods=['GET'])
@requiere_login()
def scanear_qr():
    id_reserva = request.args.get('id_reserva')
    qr_code = request.args.get('qr_code')

    try:
        r = requests.post(f"{BACKEND_URL}/reservas/validar-qr", json={
            "id_reserva": id_reserva,
            "qr_code": qr_code
        })
        mensaje = r.json().get("mensaje", "")
        exito = r.status_code == 200
    except Exception as e:
        mensaje = "Error de conexión con el servidor"
        exito = False

    return render_template('gestion/resultado_qr.html', exito=exito, mensaje=mensaje)

@admin_bp.route('/admin/dashboard/scanear-qr', methods=['GET'])
@requiere_login()
def pagina_scanear_qr():
    return render_template('gestion/scanear_qr.html') 