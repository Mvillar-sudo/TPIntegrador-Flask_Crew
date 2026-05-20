from flask import Blueprint, jsonify

menu_bp = Blueprint('menu', __name__, url_prefix='/api/menu')

@menu_bp.route('/', methods=['GET'])
def get_menu():
    return jsonify({"mensaje": "Endpoint de Menú funcionando"})

@menu_bp.route('/<int:id_plato>', methods=['GET'])
def get_plato(id_plato): 
    return jsonify({"mensaje": "Endpoint de plato encontrado"}) 

@menu_bp.route('/', methods=['POST'])
def crear_plato(): 
    return jsonify({"mensaje": "Plato creado"}) 

@menu_bp.route('/<int:id_plato>', methods=['PUT'])
def modificar_plato(id_plato): 
    return jsonify({"mensaje": "Endpoint de plato modificado"})
