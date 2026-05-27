import qrcode
import os
import textwrap

def generar_qr(id_reserva, nombre, fecha, hora, cantidad_personas, token_cancelacion):
    
    # contenido que va adentro del QR
    contenido = textwrap.dedent(f"""\
        Reserva #{id_reserva}
        Nombre: {nombre}
        Fecha: {fecha}
        Hora: {hora}
        Personas: {cantidad_personas}
        Token: {token_cancelacion}
    """)

    # generar el QR
    qr = qrcode.make(contenido)

    # carpeta donde se guardan los QR
    carpeta = "app/static/qr"
    os.makedirs(carpeta, exist_ok=True)  # crea la carpeta si no existe

    ruta = os.path.join(carpeta, f"reserva_{id_reserva}.png")
    qr.save(ruta)

    return ruta
