# 1. Hipótesis y Supuestos del Proyecto

Para el desarrollo del sistema se tendrán en cuenta los siguientes supuestos y condiciones de trabajo:

- Se asume que los clientes contarán con acceso a internet y una dirección de correo electrónico válida para recibir las confirmaciones de reserva.

- Se considera que las reservas serán realizadas principalmente desde dispositivos móviles o computadoras personales.

- El sistema estará dividido en un frontend y un backend desarrollados con Flask, comunicados mediante endpoints REST y utilizando JSON para el intercambio de información.

- La información del sistema será almacenada en una base de datos MySQL, utilizando tablas relacionadas para gestionar usuarios, reservas, menú, reseñas y servicios del local.

- El sistema contará con distintos niveles de acceso. El administrador podrá realizar operaciones de ABM y gestionar el contenido del sitio.

- Cada reserva realizada generará un código QR que será enviado al usuario por correo electrónico junto con la confirmación de la reserva.

- Se supone que el personal del local dispondrá de dispositivos con cámara y conexión a internet para validar los códigos QR generados por el sistema.

- El desarrollo del proyecto se realizará de manera grupal utilizando GitHub para el control de versiones y un tablero Kanban para la organización y seguimiento de tareas.

- Las dependencias necesarias para ejecutar el proyecto estarán detalladas en un archivo `init.sh` para facilitar la instalación y ejecución del sistema.

- Se supone que el sistema manejará un volumen moderado de reservas, acorde a un establecimiento gastronómico pequeño o mediano.

- Durante el desarrollo se buscará mantener un código modular y ordenado, evitando variables globales, ciclos infinitos y código repetido, siguiendo las buenas prácticas solicitadas por la cátedra.

# 2. Alcance del Proyecto

El objetivo del proyecto es desarrollar un sitio web gastronómico que permita a los usuarios consultar información del local y realizar reservas online, mientras que los administradores podrán gestionar el contenido y visualizar estadísticas relacionadas con el funcionamiento del sistema.

## 2.1 Funcionalidades del Frontend

- **Página Principal:** Visualización de información del local, imágenes, reseñas y servicios disponibles, como estacionamiento o acceso para personas con movilidad reducida.

- **Menú Digital:** Visualización de platos con precios, imágenes y detalle de restricciones alimenticias.

- **Sistema de Reservas:** Selección de fecha, horario y cantidad de personas para realizar reservas online de manera rápida y sencilla.

- **Confirmación de Reserva:** El usuario podrá visualizar desde la interfaz la confirmación de la reserva realizada y acceder a la información asociada.

- **Cancelación de Reservas:** Posibilidad de cancelar una reserva desde un enlace disponible en el correo recibido.

- **Reseñas de Usuarios:** Los usuarios podrán publicar opiniones y valoraciones luego de asistir al local y validar su reserva.

## 2.2 Funcionalidades del Backend

- **API REST:** Desarrollo de endpoints REST para la comunicación entre el frontend y la base de datos utilizando formato JSON.

- **Gestión de Usuarios:** Administración de usuarios y control de acceso según el rol correspondiente.

- **Gestión de Reservas:** Creación, modificación, cancelación y validación de reservas realizadas por los clientes.

- **Gestión del Menú:** Administración de platos, precios, imágenes y restricciones alimenticias.

- **Gestión de Reseñas:** Registro y almacenamiento de reseñas realizadas por usuarios que hayan asistido al local.

- **Generación de QR:** Creación automática de códigos QR asociados a cada reserva confirmada.

- **Envío de Correos:** Integración con un servicio de correo electrónico para el envío de confirmaciones y cancelaciones de reservas.

- **Conexión con Base de Datos:** Integración con MySQL para el almacenamiento y consulta de la información del sistema.

- **Validaciones y Seguridad:** Validación de datos recibidos desde el frontend y protección de endpoints según el tipo de usuario.

## 2.3 Funcionalidades del Panel Administrador

- **ABM del Menú y Servicios:** Gestión de platos, imágenes, restricciones alimenticias y servicios adicionales del establecimiento.

- **Gestión de Reseñas:** Administración y moderación de comentarios realizados por los usuarios.

- **Estadísticas de Reservas:** Visualización de información sobre reservas realizadas, historial y cancelaciones.

- **Control de Disponibilidad:** Administración de horarios y cupos disponibles para las reservas.

- **Validación mediante QR:** Escaneo y validación de códigos QR al momento de la llegada del cliente al local.

- **Gestión General del Sitio:** Modificación de información visible en el frontend y administración de usuarios con acceso al sistema.
