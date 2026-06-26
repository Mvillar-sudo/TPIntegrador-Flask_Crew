"""WSGI entry point para Gunicorn"""
from webapp import create_app

app = create_app()
