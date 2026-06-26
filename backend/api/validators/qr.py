import qrcode
import os
import textwrap
import json
from ..config import QR_FOLDER

def generar_qr(id_reserva, nombre, fecha, hora, cantidad_personas, token_cancelacion):
    
   # carpeta donde se guardan los QR
    carpeta = QR_FOLDER
    os.makedirs(carpeta, exist_ok=True)  # crea la carpeta si no existe
    ruta_qr = os.path.join(carpeta, f"reserva_{id_reserva}.png")

    contenido = json.dumps({
        "id_reserva": id_reserva,
        "qr_code": ruta_qr
    })

    qr = qrcode.make(contenido)

    qr.save(ruta_qr)

    return ruta_qr