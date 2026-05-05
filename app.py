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
        with st.spinner("🤖 Procesando... esto tarda unos 40 segundos."):
            try:
                # Esta es la versión exacta que necesitamos
                output = replicate.run(
                    "yisol/idm-vton:c8718e02",
                    input={
                        "human_img": usuario,
                        "garm_img": prenda,
                        "garment_des": "una prenda",
                        "is_checked": True
                    }
                )
                if output:
                    st.image(output[0], caption="¡Resultado!", use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Toma ambas fotos primero.")
