import streamlit as st
import replicate
import os

st.set_page_config(page_title="Probador IA", layout="centered")
st.title("👕 Probador Virtual Pro")

# Configuración de la llave
token = st.secrets.get("REPLICATE_API_TOKEN")
if token:
    os.environ["REPLICATE_API_TOKEN"] = token
else:
    st.error("Falta la llave en Secrets.")

# Interfaz
prenda = st.camera_input("1. Foto de la Prenda")
usuario = st.camera_input("2. Tu Foto")

if st.button("3. ¡VER RESULTADO!"):
    if prenda and usuario:
        with st.spinner("🤖 Procesando... esto tarda 40 segundos."):
            try:
                # Usamos la versión más estable y pública
                model = replicate.models.get("yisol/idm-vton")
                version = model.versions.get("90656041")
                
                output = version.predict(
                    human_img=usuario,
                    garm_img=prenda,
                    garment_des="una prenda",
                    is_checked=True
                )
                
                if output:
                    st.image(output[0], caption="¡Listo!", use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Faltan las fotos.")
