from flask import session


def auth_headers():
    """Devuelve Authorization header usando token en session si existe."""
    token = session.get('token')
    if token:
        return {'Authorization': f'Bearer {token}'}
    return {}
