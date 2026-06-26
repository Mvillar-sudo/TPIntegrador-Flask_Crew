from functools import wraps
from flask import request, jsonify
import jwt
from .db import query_db
from .services.auth_service import JWT_SECRET


def obtener_usuario_por_email(email):
    resultado = query_db("SELECT * FROM usuarios WHERE email = %s", (email,))
    if resultado and isinstance(resultado, list) and len(resultado) > 0:
        return resultado[0]
    return None


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"mensaje": "Token no provisto"}), 401
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({"mensaje": "Formato de token inválido"}), 401
        token = parts[1]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            email = payload.get('sub')
            if not email:
                return jsonify({"mensaje": "Token inválido"}), 401
            usuario = obtener_usuario_por_email(email)
            if not usuario or not usuario.get('activo'):
                return jsonify({"mensaje": "Acceso denegado: usuario no autorizado"}), 403
            # usuario válido y activo -> permitir
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({"mensaje": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"mensaje": "Token inválido"}), 401
        except Exception as e:
            return jsonify({"mensaje": f"Error verificando token: {str(e)}"}), 401
    return decorated
