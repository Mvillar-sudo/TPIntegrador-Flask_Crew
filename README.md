# TPIntegrador - Flask Crew 🚀

Este proyecto es una aplicación web de un restaurante. La estructura del proyecto está dividida en dos componentes principales para mantener la independencia del desarrollo y entorno: **Backend** (API y lógica de negocio) y **Frontend** (Vistas y plantillas con Jinja/JS).

---

## 📁 Estructura del Proyecto

- **`backend/`**: Servidor de la API, conexión a base de datos MySQL, lógica de servicios y validadores.
- **`frontend/`**: Interfaz de usuario que consume la API del backend, usando plantillas HTML dinámicas con Jinja y archivos estáticos (CSS/JS).
- **`docs/`**: Documentación complementaria del proyecto (Supuestos, alcances, etc.).

---

## 🛠️ Requisitos Previos

Tener instalado en el sistema:

- Python 3.10 o superior
- `pip` (Administrador de paquetes de Python)

---

## 🚀 Inicialización y Configuración

Script automatizado para crear los entornos virtuales (`venv`) e instalar las dependencias requeridas para cada componente por separado.

Para configurar todo el proyecto de una sola vez, ejecutar desde la carpeta raíz:

```bash
./init.sh
```

---

## 💻 Cómo Ejecutar la Aplicación

Para poner en marcha la aplicación, se deben iniciar ambos servidores en terminales separadas:

### 1. Levantar el Backend (API)

El backend corre por defecto en el puerto `5000`.

**Paso a paso:**

```bash
# Navegar al directorio de backend
cd backend

# Activar el entorno virtual
source venv/bin/activate

# Iniciar la aplicación
python app/app.py
```

**O en una sola línea:**

```bash
cd backend && source venv/bin/activate && python app/app.py
```

### 2. Levantar el Frontend (UI)

El frontend corre por defecto en el puerto `3000`.

**Paso a paso:**

```bash
# Navegar al directorio de frontend
cd frontend

# Activar el entorno virtual
source venv/bin/activate

# Iniciar la aplicación
python app/app.py
```

**O en una sola línea:**

```bash
cd frontend && source venv/bin/activate && python app/app.py
```

---

## ⚡ Ejecución en un solo comando (Opcional)

Para levantar ambos servidores al mismo tiempo en una sola terminal, utilizar el script `run.sh` ubicado en la raíz del proyecto.

1. Dar permisos de ejecución la primera vez:
   ```bash
   chmod +x run.sh
   ```
2. Ejecutar:
   ```bash
   ./run.sh
   ```
   _(Para detener ambos servidores a la vez, presionar `Ctrl+C` en esa misma terminal)._

---

## 📦 Dependencias Principales

- **Backend**: `Flask`, `python-dotenv`, `mysql-connector-python`, `flask-cors`.
- **Frontend**: `Flask` (con motor de plantillas `Jinja2`), `python-dotenv`.
