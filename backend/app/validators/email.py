from flask_mail import Message
from flask import current_app
from config import MAIL_USERNAME
from extensions import mail
import os

def enviar_email_reserva(email, nombre, fecha, hora, cantidad_personas, token_cancelacion, id_reserva, ruta_qr):

    # 1. armar el link de cancelación
    link_cancelacion = f"http://localhost:3000/reservas/cancelar/{token_cancelacion}"

    # 2. armar el cuerpo del email (texto plano)
    cuerpo = f"""
    Hola {nombre}, gracias por reservar en Flask Burger.

    Tu reserva ha sido confirmada con los siguientes datos:
    Fecha: {fecha}
    Hora: {hora}
    Personas: {cantidad_personas}

    Si querés cancelar o modificar tu reserva, hacé clic en el siguiente enlace:
    {link_cancelacion}

    Recordá que, para modificar tu reserva, primero tenés que cancelarla y luego crear una nueva con los datos correctos.
    Mostrá el QR adjunto al llegar al local para que podamos validar tu reserva.

    ¡Te esperamos!
    Saludos,
    El equipo de Flask Burger
    """

    # 3. crear el mensaje
    msg = Message(
        subject="Confirmación de reserva",
        sender=MAIL_USERNAME,
        recipients=[email],
        body=cuerpo, 
        charset='utf-8'
    )
    msg.body = cuerpo.encode('utf-8').decode('utf-8')
    # 4. adjuntar el QR
    try:
        with open(ruta_qr, "rb") as qr:
            msg.attach(
                filename=f"reserva_{id_reserva}.png",
                content_type="image/png",
                data=qr.read()
            )
    except FileNotFoundError:
        print(f"No se encontró el QR para la reserva {id_reserva}")

    # 5. enviar
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Error al enviar el correo: {e}")