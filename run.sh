#!/bin/bash

echo "🚀 === INICIANDO SERVIDORES ==="

# Función para cerrar los servidores
function cerrar_servidores {
  echo -e "\n🛑 Deteniendo servidores y base de datos..."
  kill $backend_pid $frontend_pid 2>/dev/null
  echo "🛑 Apagando MySQL..."
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || -f /c/xampp/mysql/bin/mysqladmin.exe ]]; then
    /c/xampp/mysql/bin/mysqladmin.exe -u root shutdown 2>/dev/null
  else
    sudo systemctl stop mysql 2>/dev/null || sudo service mysql stop 2>/dev/null
  fi
}
# Captura SIGINT, SIGTERM y EXIT para invocar la función cerrar_servidores
trap cerrar_servidores SIGINT SIGTERM EXIT

# 0. Levantar MySQL
echo "🗄️  Iniciando Base de Datos MySQL..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || -f /c/xampp/mysql/bin/mysqld.exe ]]; then
  echo "   → Detectado Windows (XAMPP)"
  /c/xampp/mysql/bin/mysqld.exe &
else
  echo "   → Detectado Linux"
  sudo systemctl start mysql 2>/dev/null || sudo service mysql start 2>/dev/null
fi
sleep 2 # Dar tiempo a que levante la base de datos

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

