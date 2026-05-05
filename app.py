import streamlit as st
import replicate
import os

st.set_page_config(page_title="Probador IA", layout="centered")
st.title("👕 Probador Virtual Pro")

# Conexión con la llave secreta
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
else:
    st.error("⚠️ Configura la llave en Secrets (Manage app > Settings).")

# Interfaz
prenda = st.camera_input("1. Foto de la Prenda", key="cam1")
usuario = st.camera_input("2. Tu Foto", key="cam2")

if st.button("3. ¡VER RESULTADO!"):
    if prenda and usuario:
        # Aquí es donde realmente se llama a la IA
        with st.spinner("🤖 La IA está trabajando... tarda unos 30-40 segundos."):
            try:
                output = replicate.run(
                    "yisol/idm-vton:c8718e02",
                    input={
                        "human_img": usuario,
                        "garm_img": prenda,
                        "garment_des": "una casaca",
                        "is_checked": True
                    }
                )
                st.image(output[0], caption="Resultado Final", use_container_width=True)
                st.success("¡Listo!")
            except Exception as e:
                st.error(f"Hubo un error técnico: {e}")
    else:
        st.warning("Toma ambas fotos primero.")
