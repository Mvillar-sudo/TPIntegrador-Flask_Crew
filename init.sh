#!/bin/bash
echo "🚀 === INICIALIZANDO ENTORNO DEL PROYECTO ==="

# Verificar si Python 3 está instalado
if ! command -v python3 &> /dev/null
then
    echo "❌ Error: Python 3 no está instalado en este sistema."
    echo "Por favor instalalo antes de continuar (ej: 'sudo apt install python3 python3-venv' en Ubuntu/Debian)."
    exit 1
fi

# 1. Configurar el Backend
echo -e "\n📦 1/2. Configurando el Backend..."
cd backend
python3 -m venv venv
source venv/bin/activate || source venv/Scripts/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
cd ..

# 2. Configurar el Frontend
echo -e "\n🎨 2/2. Configurando el Frontend (Jinja/JS)..."
cd frontend
python3 -m venv venv
source venv/bin/activate || source venv/Scripts/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
cd ..

echo -e "\n✅ === ¡ENTORNO LISTO! ==="
echo "• Para correr el Back: cd backend && source venv/bin/activate && python app/app.py"
echo "• Para correr el Front: cd frontend && source venv/bin/activate && python app/app.py"