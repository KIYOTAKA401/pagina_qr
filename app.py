import streamlit as st
from supabase import create_client, Client
import json

# Conexión a Supabase
URL = "https://azwanfinaeztivngsnlv.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF6d2FuZmluYWV6dGl2bmdzbmx2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg0OTE0MDEsImV4cCI6MjA2NDA2NzQwMX0.w9QmRZh_dro2xd9J85NYHamgzOkaKGXDN01SwCbdkEI"
supabase: Client = create_client(URL, KEY)

st.title("📥 Registro QR en Supabase")

# Manejo de POST desde el lector
if st.request.method == "POST":
    try:
        data = json.loads(st.request.body)
        valor_qr = data.get("valor_qr")
        if valor_qr:
            supabase.table("registro_qr").insert({"valor_qr": valor_qr}).execute()
            st.success(f"Valor QR recibido y guardado: {valor_qr}")
    except Exception as e:
        st.error(f"Error procesando QR: {e}")

# Campo adicional
numero_cuenta = st.text_input("Número de cuenta del estudiante (opcional)")
if st.button("Enviar número de cuenta"):
    if numero_cuenta:
        supabase.table("registro_qr").insert({"valor_qr": "manual", "numero_cuenta": numero_cuenta}).execute()
        st.success("Número de cuenta enviado")

# Mostrar registros
st.subheader("📄 Registros guardados")
data = supabase.table("registro_qr").select("*").order("created_at", desc=True).execute()
registros = data.data
for registro in registros:
    st.json(registro)
