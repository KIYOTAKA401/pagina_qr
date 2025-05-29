import cv2
from pyzbar.pyzbar import decode
import requests

def leer_qr_y_enviar(url_destino):
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        for codigo in decode(frame):
            valor = codigo.data.decode('utf-8')
            print(f"QR Detectado: {valor}")
            # Envía el valor a la URL destino
            requests.post(url_destino, json={"valor_qr": valor})
            cap.release()
            return

if __name__ == "__main__":
    # Cambia esta URL por la dirección pública de tu app de Streamlit (ej. usando ngrok o Streamlit Cloud)
    leer_qr_y_enviar("http://localhost:8501")
