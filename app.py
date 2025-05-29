import streamlit as st
import cv2
from pyzbar.pyzbar import decode
import requests
import json
import numpy as np
from PIL import Image
import time

# Configuración Supabase
SUPABASE_URL = "https://azwanfinaeztivngsnlv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF6d2FuZmluYWV6dGl2bmdzbmx2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg0OTE0MDEsImV4cCI6MjA2NDA2NzQwMX0.w9QmRZh_dro2xd9J85NYHamgzOkaKGXDN01SwCbdkEI"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Endpoint de la tabla
TABLA_ENDPOINT = f"{SUPABASE_URL}/rest/v1/registro_qr"

# Configuración de la página
st.set_page_config(page_title="Registro QR", layout="wide")
st.title("📥 Sistema de Registro con QR")

# Función para enviar datos a Supabase
def enviar_a_supabase(valor_qr, numero_cuenta=None):
    body = {"valor_qr": valor_qr}
    if numero_cuenta:
        body["numero_cuenta"] = numero_cuenta
    
    try:
        response = requests.post(TABLA_ENDPOINT, headers=HEADERS, data=json.dumps(body))
        if response.status_code in [200, 201]:
            return True, "Datos enviados correctamente"
        else:
            return False, f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return False, f"Error de conexión: {str(e)}"

# Función para leer códigos QR
def leer_qr():
    cap = cv2.VideoCapture(0)
    qr_detectado = None
    frame_placeholder = st.empty()
    stop_button = st.button("Detener lectura QR")
    
    while cap.isOpened() and not stop_button:
        ret, frame = cap.read()
        if not ret:
            st.error("No se puede acceder a la cámara")
            break
        
        # Convertir frame a RGB para mostrar en Streamlit
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)
        
        # Detectar códigos QR
        for codigo in decode(frame):
            valor = codigo.data.decode('utf-8')
            qr_detectado = valor
            # Dibujar rectángulo alrededor del QR
            pts = np.array([codigo.polygon], np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(frame, [pts], True, (0,255,0), 3)
            
            # Mostrar frame con detección
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)
            break
        
        if qr_detectado:
            break
        
        time.sleep(0.1)
    
    cap.release()
    return qr_detectado

# Interfaz principal
tab1, tab2 = st.tabs(["Lector QR", "Registros"])

with tab1:
    st.header("📷 Lector de Códigos QR")
    
    # Campo adicional para número de cuenta
    numero_cuenta = st.text_input("Número de cuenta del estudiante (opcional)")
    
    if st.button("Iniciar lectura de QR"):
        valor_qr = leer_qr()
        if valor_qr:
            st.success(f"Código QR detectado: {valor_qr}")
            exito, mensaje = enviar_a_supabase(valor_qr, numero_cuenta)
            if exito:
                st.success(mensaje)
            else:
                st.error(mensaje)
    
    # También permitir entrada manual
    with st.expander("O ingresar valor manualmente"):
        valor_manual = st.text_input("Valor QR manual")
        if st.button("Enviar manualmente") and valor_manual:
            exito, mensaje = enviar_a_supabase(valor_manual, numero_cuenta)
            if exito:
                st.success(mensaje)
            else:
                st.error(mensaje)

with tab2:
    st.header("📄 Registros guardados")
    
    # Actualizar registros
    if st.button("Actualizar registros"):
        st.experimental_rerun()
    
    try:
        response = requests.get(TABLA_ENDPOINT + "?select=*&order=created_at.desc", headers=HEADERS)
        if response.status_code == 200:
            registros = response.json()
            if registros:
                st.dataframe(registros)
            else:
                st.info("No hay registros aún")
        else:
            st.error(f"Error obteniendo registros: {response.text}")
    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")
