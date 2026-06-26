from ..db import execute_db, query_db
from werkzeug.security import check_password_hash, generate_password_hash
import os
import datetime
import jwt
JWT_SECRET = os.getenv("JWT_SECRET", "clave_por_defecto_si_no_hay_env")

def generar_jwt(usuario_email):
    payload = {
        "sub": usuario_email,  # El 'subject' o dueño del token
        "iat": datetime.datetime.now(datetime.timezone.utc),  # Cuándo se creó
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)  # Cuándo expira
    }
    # Codificamos el token usando el algoritmo HS256
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def post_login(data):
    email_usuario = data["email"] 
    password = data["password"]

    query = "SELECT email, password FROM usuarios WHERE email = %s AND activo = TRUE"
    resultado = query_db(query, (email_usuario,))

    if not resultado:
        return None

    user_db = resultado[0]

    if check_password_hash(user_db["password"], password):
        token = generar_jwt(user_db["email"])
        return {
            "token": token,
            "usuario": {
                "email": user_db["email"]
            }
        }
    return None

def post_register(data):
    email_usuario = data["email"] 
    password = data["password"]
    password_hash = generate_password_hash(password)

    query = "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)"
    nombre = data.get("nombre") or email_usuario.split("@")[0] 
    args = (nombre, email_usuario, password_hash)

    execute_db(query, args)
    return "Usuario registrado correctamente" 

def obtener_total_usuarios():
    try:
        resultado = query_db("""
            SELECT COUNT(*) as total 
            FROM usuarios 
            WHERE activo = 1
        """, one=True)
        
        if resultado:
            if isinstance(resultado, dict):
                return resultado.get('total', 0)
            return resultado[0] 
        return 0
    except Exception as e:
        print(f"⚠️ Error en auth_service al contar usuarios activos: {e}")
        return 0 
    
def obtener_usuarios():
    return query_db("""
        SELECT *
        FROM usuarios
    """) 

def obtener_usuario(id_usuario):

    query = "SELECT * FROM usuarios WHERE id_usuario = %s;"
    args = (id_usuario,)

    usuario = query_db(query, args) 

    if usuario and isinstance(usuario, list):
        return usuario[0]

    return None

def actualizar_usuario(id_usuario, data):

    nombre = data.get('nombre')
    email = data.get("email")

    # Hash password only if provided; otherwise leave unchanged
    password_plain = data.get('password')
    password_hash = generate_password_hash(password_plain) if password_plain else None

    # Only change 'activo' if the key is present in payload. Otherwise keep current value.
    if 'activo' in data:
        activo_val = 1 if data.get('activo') in (True, 1, '1', 'True', 'true') else 0
    else:
        activo_val = None

    return execute_db("""
        UPDATE usuarios
        SET nombre = COALESCE(%s, nombre),
            email = COALESCE(%s, email),
            password = COALESCE(%s, password),
            activo = COALESCE(%s, activo)
        WHERE id_usuario = %s
    """, (nombre, email, password_hash, activo_val, id_usuario)) 

def eliminar_usuario(id_usuario):
       return execute_db(
        "DELETE FROM usuarios WHERE id_usuario = %s",
        (id_usuario,)
    ) 
