#!/bin/bash

echo "🚀 === INICIANDO SERVIDORES ==="

# Función para cerrar los servidores
function cerrar_servidores {
  echo -e "\n🛑 Deteniendo servidores..."
  kill $backend_pid $frontend_pid 2>/dev/null
}
# Captura SIGINT, SIGTERM y EXIT para invocar la función cerrar_servidores
trap cerrar_servidores SIGINT SIGTERM EXIT

# 1. Levantar el Backend en segundo plano
echo "📡 Iniciando Servidor Backend (Puerto 5000)..."
cd backend
source venv/bin/activate || source venv/Scripts/activate
python app/app.py &
backend_pid=$!
cd ..

# 2. Levantar el Frontend en segundo plano
echo "🎨 Iniciando Servidor Frontend (Puerto 3000)..."
cd frontend
source venv/bin/activate || source venv/Scripts/activate
python app/app.py &
frontend_pid=$!
cd ..

sleep 1.5

echo -e "\n✅ Ambos servidores iniciados con éxito:"
echo "• Backend: http://localhost:5000"
echo "• Frontend: http://localhost:3000"
echo "Presiona [Ctrl+C] en esta terminal para detener ambos servidores a la vez."
wait $backend_pid $frontend_pid

