from flask_mail import Message
from flask import current_app
from app.config import MAIL_USERNAME
from app import mail
import os

def enviar_email_reserva(email, nombre, fecha, hora, cantidad_personas, token_cancelacion, id_reserva):

    # 1. armar el link de cancelación
    link_cancelacion = f"http://localhost:5000/api/reservas/cancelar/{token_cancelacion}"

    # 2. armar el cuerpo del email
    cuerpo = f"""
    Hola {nombre}, tu reserva fue confirmada.
    
    Fecha: {fecha}
    Hora: {hora}
    Personas: {cantidad_personas}
    
    Para cancelar tu reserva hacé click acá:
    {link_cancelacion}
    """

    # 3. crear el mensaje
    msg = Message(
        subject="Confirmación de reserva",
        sender=MAIL_USERNAME,
        recipients=[email],
        body=cuerpo
    )

    # 4. adjuntar el QR
    ruta_qr = f"app/static/qr/reserva_{id_reserva}.png"
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