#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== INICIANDO SERVIDORES ==="

function cerrar_servidores {
  echo -e "\nDeteniendo servidores y base de datos..."
  kill $backend_pid $frontend_pid 2>/dev/null
  echo "Apagando MySQL..."
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || -f /c/xampp/mysql/bin/mysqladmin.exe ]]; then
    /c/xampp/mysql/bin/mysqladmin.exe -u root shutdown 2>/dev/null
  else
    sudo systemctl stop mysql 2>/dev/null || sudo service mysql stop 2>/dev/null
  fi
  exit 0
}

trap cerrar_servidores SIGINT SIGTERM

echo "Iniciando Base de Datos MySQL..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || -f /c/xampp/mysql/bin/mysqld.exe ]]; then
  echo "  -> Detectado Windows (XAMPP)"
  /c/xampp/mysql/bin/mysqld.exe &
else
  echo "  -> Detectado Linux"
  sudo systemctl start mysql 2>/dev/null || sudo service mysql start 2>/dev/null
fi
sleep 2

echo "Iniciando Servidor Backend (Puerto 5000)..."
cd "$SCRIPT_DIR/backend" || exit 1
if [ -f "venv/Scripts/python.exe" ]; then
  backend_py="venv/Scripts/python.exe"
elif [ -f "venv/bin/python" ]; then
  backend_py="venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  backend_py="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  backend_py="$(command -v python)"
else
  echo "No se encontro Python para el backend (instala Python o crea el venv)."
  exit 1
fi
"$backend_py" -m api.run &
backend_pid=$!

echo "Iniciando Servidor Frontend (Puerto 3000)..."
cd "$SCRIPT_DIR/frontend" || exit 1
if [ -f "venv/Scripts/python.exe" ]; then
  frontend_py="venv/Scripts/python.exe"
elif [ -f "venv/bin/python" ]; then
  frontend_py="venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  frontend_py="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  frontend_py="$(command -v python)"
else
  echo "No se encontro Python para el frontend (instala Python o crea el venv)."
  exit 1
fi
"$frontend_py" -m webapp.run &
frontend_pid=$!

if command -v sleep >/dev/null 2>&1; then
  sleep 1
else
  read -t 1 -n 0 || true
fi

echo
echo "Ambos servidores iniciados con exito:"
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo "Presiona Ctrl+C en esta terminal para detener ambos servidores a la vez."

while true; do
  if command -v sleep >/dev/null 2>&1; then
    sleep 1
  else
    read -t 1 -n 0 || true
  fi
done
