# Proyecto Final IDS 2026C1

**Proyecto:** Sitio web gastronómico con reservas  
**Materia:** Introducción al Desarrollo de Software  
**Consigna elegida:** Opción B  
**Repositorio:** TPIntegrador-Flask_Crew

## Integrantes

- Elias Roman Cantero Castronuovo | El14sR
- Valentín Javier Alonso Marés | ValenAlonso
- Camilo Jesus Toscano Mota | tonascocamilo
- Nicolás Grinstin | NicoGrin

## Resumen

El proyecto consiste en el desarrollo de una aplicación web para un local gastronómico que permite mostrar información pública del establecimiento y, al mismo tiempo, administrar reservas, menú, reseñas, servicios y usuarios desde un panel interno.

La solución se dividió en dos componentes principales: un frontend orientado al cliente final y un backend encargado de la lógica de negocio, la seguridad, la persistencia y la exposición de una API REST. El sistema utiliza MySQL como base de datos, Flask como framework principal y un flujo de trabajo basado en endpoints JSON para comunicar ambas capas.

Entre sus funciones más importantes se destacan la navegación pública del sitio, la realización de reservas con confirmación por correo, la generación de QR para validar el ingreso, el manejo de reseñas publicadas por usuarios y un dashboard administrativo con métricas de gestión.

## Introducción

La propuesta responde a la opción B de la consigna de la cátedra: un sitio web gastronómico con reservas. El objetivo es resolver la necesidad de un restaurante de mostrar su propuesta al público, centralizar la toma de reservas y permitir que el equipo administrativo administre la información del local sin depender de cambios manuales sobre el sitio.

Durante el desarrollo se priorizó una arquitectura separada por responsabilidades. El frontend se encarga de la experiencia visual y de la interacción con el usuario, mientras que el backend concentra la lógica de negocio y el acceso a la base de datos. Esta separación facilita el mantenimiento, la escalabilidad y la depuración de errores.

También se tuvieron en cuenta los requisitos de la cátedra vinculados con GitHub, el uso de MySQL, la modularización del código, la existencia de scripts para instalar dependencias y ejecutar el sistema, y la generación de un informe final con las decisiones más relevantes del proyecto.

## Solución propuesta

La aplicación propone una experiencia completa para un restaurante:

- Una página pública con información general del local.
- Un menú digital con platos, precios, imágenes y disponibilidad.
- Un sistema de reservas simple y rápido.
- Envío de confirmación por correo electrónico.
- Generación de QR asociado a cada reserva.
- Cancelación de reservas desde el enlace recibido por correo.
- Reseñas publicadas por clientes.
- Panel de administración con ABM de menú, servicios, usuarios y reseñas.
- Dashboard con métricas útiles para control operativo.

## Arquitectura general

La aplicación se organizó en dos proyectos Flask independientes:

- `backend/`: expone la API REST, valida datos, administra la autenticación y se conecta a MySQL.
- `frontend/`: renderiza las vistas, consume la API y presenta la interfaz del usuario final y del administrador.

La comunicación entre ambos se realiza mediante solicitudes HTTP y formato JSON. Esta decisión permite que el frontend no dependa directamente de la base de datos y que el backend quede preparado para integrarse con otras interfaces en el futuro.

## Estructura del proyecto

La estructura principal del proyecto se organizó de la siguiente manera:

- `backend/app/routes`: contiene las rutas y controladores de la API.
- `backend/app/services`: contiene la lógica de negocio.
- `backend/app/validators`: contiene funciones de validación.
- `backend/data`: contiene scripts relacionados con la base de datos (ej. `schema.sql`).
- `frontend/app/templates`: contiene las vistas HTML renderizadas por Flask.
- `frontend/app/static`: contiene archivos estáticos del frontend (CSS, imágenes).
- `frontend/webapp/static/qr`: utilizado para almacenar los códigos QR generados de las reservas.
- `docs`: contiene la documentación del proyecto, incluyendo Swagger e informes.
- `init.sh`: script para inicializar el entorno del proyecto.
- `run.sh`: script para ejecutar los componentes principales del sistema.

## Funcionalidades del frontend

- Página de inicio con información del local.
- Sección de menú con platos e imágenes.
- Formulario de reserva.
- Cancelación de reservas mediante enlace seguro.
- Formulario de reseñas.
- Panel administrativo para gestionar contenido.

## Funcionalidades del backend

- Autenticación de administradores.
- ABM de menú.
- ABM de servicios.
- ABM de reseñas.
- Gestión de reservas.
- Validación de QR.
- Envío de correos con confirmación y datos de reserva.
- Exposición de métricas para dashboard.

## Base de datos

El esquema se implementó en MySQL con tablas para:

- usuarios
- menú
- reservas
- servicios
- reseñas

Cada tabla fue pensada para cubrir una parte concreta del dominio del restaurante y mantener una estructura simple, clara y fácil de extender.

## Tecnología utilizada

### Backend

- Python 3
- Flask
- Flask-Mail
- Flask-CORS
- PyJWT
- mysql-connector-python
- python-dotenv
- qrcode

### Frontend

- Flask
- Jinja2
- requests
- python-dotenv

### Base de datos

- MySQL

### Documentación y soporte

- Swagger / OpenAPI
- Markdown para la documentación del proyecto
- GitHub para control de versiones

## Decisiones de diseño

- Se separó backend y frontend para respetar responsabilidades claras.
- Se usó Flask por su simplicidad y compatibilidad con la consigna.
- Se adoptó MySQL por ser la base de datos requerida.
- Se trabajó con endpoints REST y JSON para facilitar la integración.
- Se agregaron scripts `init.sh` y `run.sh` para simplificar instalación y ejecución.
- Se incluyó un dashboard administrativo para centralizar la gestión.
- Se generó documentación de API en formato Swagger para facilitar la revisión técnica.
- Se modularizó el backend en rutas, servicios y validadores para separar responsabilidades.

## Dificultades encontradas

Durante el desarrollo se presentaron distintas dificultades técnicas. Además, analizando los commits y el historial de cambios, identificamos las partes que tuvieron más modificaciones y correcciones (fixes), destacándose como las partes que más se nos dificultaron:

- **Sección de Administración (Admin):** Esta fue claramente la parte que más se nos dificultó. Requirió múltiples ajustes continuos tanto en las rutas del administrador (`frontend/app/rutas_admin.py`, siendo el archivo con más cambios) como en sus vistas asociadas (como `dashboard.html`). Integrar correctamente la gestión de información y seguridad tomó un esfuerzo considerable.
- **Rutas y Vistas del Cliente:** El frontend público también presentó retos, lo que se refleja en la alta cantidad de modificaciones en el enrutamiento (`frontend/app/rutas_cliente.py`) y en la estructura y estilos de las vistas (`landing.html`, `menu.html`, `style.css`).
- **Lógica de Reservas:** En el backend, la gestión y validación de las reservas (`backend/app/routes/reservas.py`) fue el módulo que más cambios requirió para asegurar un flujo estable y coordinado.
- **Configuración y Orquestación Principal:** Archivos centrales como `backend/app/app.py` y `backend/app/services/__init__.py` sufrieron muchas iteraciones al tener que integrar constantemente los distintos componentes del sistema.
- La organización de imports y paquetes requirió cuidado para evitar dependencias circulares y rutas ambiguas.
- La integración entre frontend, backend, correo electrónico y QR obligó a revisar varias veces el flujo completo de reserva.
- El manejo de imágenes y archivos estáticos requirió validar correctamente las rutas de guardado.
- La separación entre rutas, servicios y validadores necesitó consistencia para no mezclar lógica de negocio con controladores.
- La configuración de ejecución de backend y frontend requirió ordenar la estructura del proyecto para evitar conflictos entre módulos con nombres similares.

## Conclusiones

El proyecto permitió integrar de forma práctica los contenidos vistos en la materia: desarrollo web, comunicación entre frontend y backend, uso de base de datos relacional, validación de datos, autenticación y organización del trabajo en equipo.

Como resultado se obtuvo una aplicación funcional que cumple con los requisitos principales de la opción B: mostrar información pública, administrar menú y servicios, registrar reseñas, gestionar reservas con confirmación por correo y ofrecer herramientas de control para el administrador.

También se reforzó la importancia de trabajar con una arquitectura ordenada, nombres de paquetes claros, scripts de instalación reproducibles y documentación técnica actualizada. Esto no solo mejora la calidad del código, sino que facilita la corrección, el mantenimiento y la futura expansión del sistema.

En conclusión, la solución propuesta responde al objetivo del proyecto integrador y deja una base sólida para seguir agregando mejoras, validaciones y nuevas funcionalidades según las necesidades del local o de la cátedra.