import qrcode
import os
import textwrap
import json

def generar_qr(id_reserva, nombre, fecha, hora, cantidad_personas, token_cancelacion):
    
    carpeta = "app/static/qr"
    ruta = os.path.join(carpeta, f"reserva_{id_reserva}.png")

    contenido = json.dumps({
        "id_reserva": id_reserva,
        "qr_code": ruta
    })

    qr = qrcode.make(contenido)

    os.makedirs(carpeta, exist_ok=True)
    qr.save(ruta)

    return ruta