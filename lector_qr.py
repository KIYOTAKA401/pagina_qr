import cv2
from pyzbar.pyzbar import decode
import requests

# URL de la tabla Supabase REST
SUPABASE_URL = "https://azwanfinaeztivngsnlv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  # Reemplaza con tu llave real

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def leer_qr_y_enviar():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        for codigo in decode(frame):
            valor = codigo.data.decode('utf-8')
            print(f"QR Detectado: {valor}")
            # Envía directamente a Supabase
            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/registro_qr",
                headers=HEADERS,
                json={"valor_qr": valor}
            )
            print(f"Respuesta Supabase: {response.status_code} - {response.text}")
            cap.release()
            return

if __name__ == "__main__":
    leer_qr_y_enviar()
