from flask import Blueprint, request, jsonify
import mysql.connector

servicios_bp = Blueprint('servicios', __name__)

def conectar_db():
    # Aquí van los datos de conexión que acordaron en el grupo
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="tu_password",
        database="nombre_base_datos"
    )

# 1. ENDPOINT PARA MOSTRAR LOS SERVICIOS (GET)
@servicios_bp.route('/api/servicios', methods=['GET'])
def listar_servicios():
    conn = conectar_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM servicios_extras")
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultados), 200

# 2. ENDPOINT PARA AGREGAR UN SERVICIO (POST)
@servicios_bp.route('/api/servicios', methods=['POST'])
def agregar_servicio():
    datos = request.get_json()
    nombre = datos.get('nombre')
    descripcion = datos.get('descripcion')
    
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO servicios_extras (nombre, descripcion) VALUES (%s, %s)",
        (nombre, descripcion)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Servicio guardado con éxito"}), 201
