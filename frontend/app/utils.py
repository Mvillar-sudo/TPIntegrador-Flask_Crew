from functools import wraps
from flask import session, redirect, url_for, flash


def usuario_actual() -> dict:
    """Retorna el usuario logueado guardado en la sesion, o {} si no hay."""
    return session.get('usuario') or {}


def token_actual() -> str:
    """Retorna el JWT guardado en la sesion, o cadena vacia si no hay."""
    return session.get('token') or ''


def guardar_sesion(token: str, usuario: dict) -> None:
    """Persiste token y usuario en la sesion de Flask."""
    session['token']   = token
    session['usuario'] = usuario


def limpiar_sesion() -> None:
    """Borra todos los datos de autenticacion de la sesion."""
    session.pop('token', None)
    session.pop('usuario', None)


def extraer_mensajes_error(api_response: dict) -> list[str]:
    """Obtiene una lista de descripciones de error desde una respuesta de la API."""
    errores = (api_response or {}).get('errors', [])

    return [e.get('description') or e.get('message') or 'Error desconocido' for e in errores]


def codigos_error(api_response: dict) -> list[str]:
    """Obtiene la lista de 'code' de cada error retornado por la API."""
    errores = (api_response or {}).get('errors', [])

    return [e.get('code', '') for e in errores]


def requiere_login():
    """Decorador para vistas: exige sesion activa, sino redirige a /login."""
    def decorador(funcion):
        @wraps(funcion)
        def wrapper(*args, **kwargs):
            if not usuario_actual() or not token_actual():
                flash('Iniciá sesión para continuar.', 'error')

                return redirect(url_for('auth.login'))

            return funcion(*args, **kwargs)

        return wrapper

    return decorador