import qrcode
import os
import textwrap
import json

def generar_qr(id_reserva, nombre, fecha, hora, cantidad_personas, token_cancelacion):
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    carpeta = os.path.join(BASE_DIR, "frontend", "app", "static", "qr")
    ruta_qr = os.path.join(carpeta, f"reserva_{id_reserva}.png")

    contenido = json.dumps({
        "id_reserva": id_reserva,
        "qr_code": ruta_qr
    })

    qr = qrcode.make(contenido)

    os.makedirs(carpeta, exist_ok=True)
    qr.save(ruta_qr)

    return ruta_qr