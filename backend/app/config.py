import os
from dotenv import load_dotenv

load_dotenv()

# DATABASE
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'tpintegrador_db')
DB_PORT = int(os.getenv('DB_PORT', 3306))

# MAIL
MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
MAIL_USE_TLS = True
MAIL_USE_SSL= False
MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')

# RESERVAS
MAX_RESERVAS_POR_FRANJA = 10

