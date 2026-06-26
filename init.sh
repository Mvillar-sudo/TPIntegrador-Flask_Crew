#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== INICIALIZANDO ENTORNO DEL PROYECTO ==="

find_python() {
  if command -v python3 >/dev/null 2>&1; then
    command -v python3
  elif command -v python >/dev/null 2>&1; then
    command -v python
  elif command -v py >/dev/null 2>&1; then
    echo "py -3"
  else
    echo ""
  fi
}

PYTHON_CMD="$(find_python)"

if [[ -z "$PYTHON_CMD" ]]; then
  echo "Error: no se encontro Python en este sistema."
  echo "Instalalo antes de continuar."
  exit 1
fi

setup_component() {
  local component_dir="$1"
  local label="$2"
  local requirements_file="$component_dir/requirements.txt"

  echo -e "\nConfigurando $label..."
  cd "$component_dir" || exit 1

  if [[ "$PYTHON_CMD" == "py -3" ]]; then
    py -3 -m venv --clear venv
  else
    "$PYTHON_CMD" -m venv --clear venv
  fi

  if [[ -f "venv/Scripts/python.exe" ]]; then
    VENV_PY="venv/Scripts/python.exe"
  else
    VENV_PY="venv/bin/python"
  fi

  "$VENV_PY" -m pip install --upgrade pip
  "$VENV_PY" -m pip install -r "$requirements_file"
}

setup_component "$SCRIPT_DIR/backend" "Backend"
setup_component "$SCRIPT_DIR/frontend" "Frontend"

echo -e "\n=== ENTORNO LISTO ==="
echo "Para correr el backend: cd backend && python -m api.run"
echo "Para correr el frontend: cd frontend && python -m webapp.run"
