import streamlit as st
import replicate
import os

st.set_page_config(page_title="Probador IA", layout="centered")
st.title("👕 Probador Virtual Pro")

# Conexión con la llave
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("Falta la llave en Secrets.")

# Interfaz
prenda = st.camera_input("1. Foto de la Prenda", key="cam1")
usuario = st.camera_input("2. Tu Foto", key="cam2")

if st.button("3. ¡VER RESULTADO!"):
    if prenda and usuario:
        with st.spinner("🤖 La IA está trabajando... espera 30 segundos."):
            try:
                # Versión actualizada y estable del modelo IDM-VTON
                output = replicate.run(
                    "yisol/idm-vton:90656041",
                    input={
                        "human_img": usuario,
                        "garm_img": prenda,
                        "garment_des": "una prenda de vestir",
                        "is_checked": True
                    }
                )
                if output:
                    st.image(output[0], caption="Resultado Final", use_container_width=True)
                    st.success("¡Logrado!")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Toma ambas fotos primero.")
