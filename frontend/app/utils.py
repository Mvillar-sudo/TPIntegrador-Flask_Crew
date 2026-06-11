from functools import wraps
from flask import session, redirect, url_for, flash

def usuario_actual() -> dict:
    return session.get('usuario') or {}

def token_actual() -> str:
    return session.get('token') or ''

def guardar_sesion(token: str, usuario: dict) -> None:
    session['token']   = token
    session['usuario'] = usuario

def limpiar_sesion() -> None:
    session.pop('token', None)
    session.pop('usuario', None)

def extraer_mensajes_error(api_response: dict) -> list[str]:
    errores = (api_response or {}).get('errors', [])
    
    if not errores and 'mensaje' in api_response:
        return [api_response['mensaje']]
    if not errores and 'error' in api_response:
        return [api_response['error']]

    return [e.get('description') or e.get('message') or 'Error desconocido' for e in errores]

def codigos_error(api_response: dict) -> list[str]:
    errores = (api_response or {}).get('errors', [])
    return [e.get('code', '') for e in errores]

def requiere_login():
    def decorador(funcion):
        @wraps(funcion)
        def wrapper(*args, **kwargs):
            if not usuario_actual() or not token_actual():
                flash('Iniciá sesión para continuar.', 'error')
                return redirect(url_for('admin.login')) 

            return funcion(*args, **kwargs)
        return wrapper
    return decorador