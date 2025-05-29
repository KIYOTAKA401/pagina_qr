import streamlit as st
import requests
import json
import qrcode
from PIL import Image
import time

# Configuración Supabase (REEMPLAZA CON TUS DATOS)
SUPABASE_URL = "https://azwanfinaeztivngsnlv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF6d2FuZmluYWV6dGl2bmdzbmx2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg0OTE0MDEsImV4cCI6MjA2NDA2NzQwMX0.w9QmRZh_dro2xd9J85NYHamgzOkaKGXDN01SwCbdkEI"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Función para guardar en Supabase
def guardar_registro(numero_cuenta, qr_data):
    data = {
        "numero_cuenta": numero_cuenta,
        "qr_data": qr_data
    }
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/registros",
        headers=HEADERS,
        data=json.dumps(data)
    )
    return response

# Interfaz de Streamlit
st.title("📋 Registro de Asistencia")

# Paso 1: Ingresar número de cuenta
numero_cuenta = st.text_input("Número de cuenta del estudiante*", key="cuenta")

if st.button("Generar QR de Asistencia"):
    if numero_cuenta:
        # Generar QR único
        qr_data = f"ASISTENCIA-{numero_cuenta}-{int(time.time())}"
        img = qrcode.make(qr_data)
        
        # Guardar en Supabase
        response = guardar_registro(numero_cuenta, qr_data)
        
        if response.status_code == 201:
            st.success("✅ Registro exitoso!")
            
            # Mostrar QR
            st.subheader("Escanea este código para registrar asistencia:")
            st.image(img.get_image(), width=200)
            
            # Mostrar datos guardados
            st.json({
                "numero_cuenta": numero_cuenta,
                "qr_data": qr_data,
                "status": "Registrado en Supabase"
            })
        else:
            st.error(f"Error al guardar: {response.text}")
    else:
        st.warning("⚠️ Por favor ingresa un número de cuenta")

# Ver registros existentes
if st.button("Ver todos los registros"):
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/registros?select=*",
        headers=HEADERS
    )
    if response.status_code == 200:
        st.subheader("Registros en Supabase")
        st.write(response.json())
    else:
        st.error(f"Error obteniendo registros: {response.text}")
