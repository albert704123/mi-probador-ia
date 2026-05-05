import streamlit as st

st.title("Probador Virtual 3 Pasos")

# Paso 1
st.header("1. Foto de la Prenda")
prenda = st.camera_input("Captura la casaca")

# Paso 2
st.header("2. Tu Foto")
usuario = st.camera_input("Tómate una foto")

# Paso 3
if st.button("3. ¡VER RESULTADO!"):
    if prenda and usuario:
        st.success("¡Fotos recibidas! Procesando con IA...")
    else:
        st.warning("Asegúrate de tomar ambas fotos primero.")
