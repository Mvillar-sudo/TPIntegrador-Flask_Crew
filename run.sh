#!/bin/bash
echo "🚀 === INICIANDO SERVIDORES ==="


# 1. Levantar el Backend en segundo plano (&)
echo "📡 Iniciando Servidor Backend (Puerto 5000)..."
cd backend
source venv/bin/activate || source venv/Scripts/activate
python app/app.py &
cd ..

# 2. Levantar el Frontend en segundo plano (&)
echo "🎨 Iniciando Servidor Frontend (Puerto 3000)..."
cd frontend
source venv/bin/activate || source venv/Scripts/activate
python app/app.py &
cd ..

sleep 1.5

echo -e "\n✅ Ambos servidores iniciados con éxito:"
echo "• Backend: http://localhost:5000"
echo "• Frontend: http://localhost:3000"
echo "Presiona [Ctrl+C] en esta terminal para detener ambos servidores a la vez."

wait

