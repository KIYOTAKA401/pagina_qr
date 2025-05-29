import streamlit as st
import requests
import json

# Reemplaza con tu URL y API KEY correcta
SUPABASE_URL = "https://azwanfinaeztivngsnlv.supabase.co"
SUPABASE_KEY = "tu_clave_anon_correcta"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

st.title("📥 Registro QR en Supabase")

# Endpoint de la tabla
tabla_endpoint = f"{SUPABASE_URL}/rest/v1/registro_qr"

# Campo adicional
numero_cuenta = st.text_input("Número de cuenta del estudiante (opcional)")
if st.button("Enviar número de cuenta"):
    if numero_cuenta:
        body = {
            "valor_qr": "manual",
            "numero_cuenta": numero_cuenta
        }
        r = requests.post(tabla_endpoint, headers=HEADERS, data=json.dumps(body))
        if r.status_code == 201:
            st.success("Número de cuenta enviado")
        else:
            st.error(f"Error: {r.text}")

# Mostrar registros
st.subheader("📄 Registros guardados")
r = requests.get(tabla_endpoint + "?select=*", headers=HEADERS)
if r.status_code == 200:
    registros = r.json()
    for registro in registros:
        st.json(registro)
else:
    st.error("Error obteniendo registros")
