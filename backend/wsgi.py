"""WSGI entry point para Gunicorn"""
from api import create_app

app = create_app()
