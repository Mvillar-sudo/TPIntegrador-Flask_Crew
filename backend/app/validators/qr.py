import qrcode
import os
import textwrap
import json

def generar_qr(id_reserva, nombre, fecha, hora, cantidad_personas, token_cancelacion):
    
   # carpeta donde se guardan los QR
    carpeta = "app/static/qr"
    os.makedirs(carpeta, exist_ok=True)  # crea la carpeta si no existe
    ruta_qr = os.path.join(carpeta, f"reserva_{id_reserva}.png")

    contenido = json.dumps({
        "id_reserva": id_reserva,
        "qr_code": ruta_qr
    })

    qr = qrcode.make(contenido)

    qr.save(ruta_qr)

    return ruta_qr