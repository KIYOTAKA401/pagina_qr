import streamlit as st
import requests
import json
import qrcode
from PIL import Image
import time
from datetime import datetime

# Configuración Supabase
SUPABASE_URL = "https://azwanfinaeztivngsnlv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF6d2FuZmluYWV6dGl2bmdzbmx2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg0OTE0MDEsImV4cCI6MjA2NDA2NzQwMX0.w9QmRZh_dro2xd9J85NYHamgzOkaKGXDN01SwCbdkEI"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Función para buscar alumno por número de cuenta
def buscar_alumno(numero_cuenta):
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/alumnos?numero_cuenta=eq.{numero_cuenta}",
        headers=HEADERS
    )
    if response.status_code == 200 and len(response.json()) > 0:
        return response.json()[0]
    return None

# Función para guardar asistencia
def guardar_asistencia(alumno_id, qr_data):
    data = {
        "alumno_id": alumno_id,
        "qr_data": qr_data,
        "fecha": datetime.now().isoformat()
    }
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/asistencias",
        headers=HEADERS,
        data=json.dumps(data)
    )
    return response

# Función opcional para guardar en registros (logs)
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

numero_cuenta = st.text_input("Número de cuenta del estudiante*", key="cuenta")

if st.button("Generar QR de Asistencia"):
    if numero_cuenta:
        # Buscar alumno
        alumno = buscar_alumno(numero_cuenta)
        
        if alumno:
            # Generar QR único
            qr_data = f"ASISTENCIA-{numero_cuenta}-{int(time.time())}"
            img = qrcode.make(qr_data)
            
            # Guardar asistencia
            response = guardar_asistencia(alumno['id'], qr_data)
            
            if response.status_code == 201:
                st.success(f"✅ Asistencia registrada para {alumno['nombre']}!")
                
                # Mostrar QR
                st.subheader("Escanea este código para registrar asistencia:")
                st.image(img.get_image(), width=200)
                
                # Opcional: Guardar en registros (logs)
                guardar_registro(numero_cuenta, qr_data)
            else:
                st.error(f"Error al guardar asistencia: {response.text}")
        else:
            st.error("❌ No se encontró un alumno con ese número de cuenta")
    else:
        st.warning("⚠️ Por favor ingresa un número de cuenta")

# Ver asistencias
if st.button("Ver todas las asistencias"):
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/asistencias?select=*,alumnos(nombre,numero_cuenta)",
        headers=HEADERS
    )
    if response.status_code == 200:
        st.subheader("Registros de Asistencia")
        st.write(response.json())
    else:
        st.error(f"Error obteniendo asistencias: {response.text}")
