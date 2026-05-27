from flask import Blueprint, render_template, request, redirect, url_for, session

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/login')
def login():
    return render_template('login.html')

@admin_bp.route('/admin/login_process', methods=['POST'])
def login_process():
    usuario = request.form.get('username')
    contrasena = request.form.get('password')
    
    if usuario == "admin" and contrasena == "123":
        session['admin_logeado'] = True
        return redirect(url_for('admin.dashboard')) 

@admin_bp.route('/admin/dashboard')
def dashboard():
    if not session.get('admin_logeado'):
        return redirect(url_for('admin.login'))
        
    return render_template('gestion/dashboard.html')

@admin_bp.route('/admin/dashboard/menu')
def menu():
    if not session.get('admin_logeado'): 
        return redirect(url_for('admin.login'))
    
    platos = [
        {
            "id": 1, 
            "nombre": "Fresh Mushrooms", 
            "precio": 19.15, 
            "descripcion": "Far far away, behind the word...", 
            "activo": True, 
            "fecha_creacion": "2026-01-15"
        },
        {
            "id": 2, 
            "nombre": "Cheese and Garlic Toast", 
            "precio": 20.99, 
            "descripcion": "Delicious toast with garlic butter...", 
            "activo": True, 
            "fecha_creacion": "2026-02-20"
        }
    ]
    return render_template('gestion/menu.html', platos=platos)


@admin_bp.route('/admin/dashboard/reservas')
def reservas():
    if not session.get('admin_logeado'): 
        return redirect(url_for('admin.login'))
        
    reservas_lista = [
        {
            "id": 101, 
            "email": "juan@email.com", 
            "fecha": "2026-05-28", 
            "hora": "21:00", 
            "cantidad_personas": 4, 
            "estado": "Confirmada",
            "token_cancelacion": "xyz789token",
            "qr_code": "qr_reserva_101.png",
            "fecha_creacion": "2026-05-25"
        }
    ]
    return render_template('gestion/reservas.html', reservas=reservas_lista)


@admin_bp.route('/admin/dashboard/servicios')
def servicios():
    if not session.get('admin_logeado'): 
        return redirect(url_for('admin.login'))
        
    servicios_lista = [
        {"id": 1, "nombre": "Catering Eventos", "activo": True, "fecha_creacion": "2026-03-01"},
        {"id": 2, "nombre": "Delivery VIP", "activo": False, "fecha_creacion": "2026-04-10"}
    ]
    return render_template('gestion/servicios.html', servicios=servicios_lista)