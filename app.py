import streamlit as st
import replicate
import os
import requests
from PIL import Image
import io
import base64

st.set_page_config(page_title="Probador IA", layout="centered")
st.title("👕 Probador Virtual Pro")

# Configuración de la llave
token = st.secrets.get("REPLICATE_API_TOKEN")
if token:
    os.environ["REPLICATE_API_TOKEN"] = token
else:
    st.error("Falta la llave en Secrets.")
    st.stop()

# Función para convertir imagen subida a URL pública (temporal)
def upload_to_temp_url(image_file):
    """Sube la imagen a un servicio temporal y devuelve URL"""
    # Opción 1: Usar temp.images (gratis, sin registro)
    files = {'file': image_file.getvalue()}
    response = requests.post('https://temp.images/upload', files=files)
    if response.status_code == 200:
        return response.json()['url']
    else:
        # Opción 2: Convertir a base64 si falla el hosting
        return f"data:image/jpeg;base64,{base64.b64encode(image_file.getvalue()).decode()}"

# Función para preprocesar la imagen de persona (opcional pero recomendado)
def preprocess_person_image(image_file):
    """Redimensiona y convierte a formato adecuado"""
    img = Image.open(image_file)
    # Redimensionar manteniendo aspecto, máximo 1024px
    img.thumbnail((1024, 1024))
    # Convertir a RGB
    if img.mode != 'RGB':
        img = img.convert('RGB')
    # Guardar en buffer
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=85)
    return buf.getvalue()

# Interfaz
st.write("### 📸 Toma tus fotos")
col1, col2 = st.columns(2)

with col1:
    prenda = st.camera_input("📍 Prenda (fondo claro ideal)")
    if prenda:
        st.image(prenda, caption="Prenda cargada", width=200)

with col2:
    usuario = st.camera_input("📍 Tú (cuerpo entero, brazos separados)")
    if usuario:
        st.image(usuario, caption="Tu foto cargada", width=200)

# Opciones avanzadas
with st.expander("⚙️ Opciones avanzadas"):
    garment_type = st.selectbox(
        "Tipo de prenda",
        ["una camisa", "un pantalón", "un vestido", "una chaqueta", "una falda"]
    )
    is_checked = st.checkbox("Prenda ya recortada (sin fondo)", value=False)

if st.button("👗 ¡VER RESULTADO!", type="primary"):
    if not prenda or not usuario:
        st.warning("📸 Toma ambas fotos primero.")
        st.stop()
    
    # Preprocesar imágenes
    with st.spinner("🔄 Preparando imágenes..."):
        try:
            # Preprocesar foto de persona (opcional, mejora resultados)
            persona_bytes = preprocess_person_image(usuario)
            # Crear archivo temporal style
            from io import BytesIO
            persona_file = BytesIO(persona_bytes)
            
            # Subir a URL temporal (necesario para Replicate)
            # NOTA: Replicate también acepta archivos localmente si usas `open()`, pero en Streamlit Cloud necesitas URLs
            # Por simplicidad, convertimos a base64 (funciona pero puede ser lento)
            def img_to_base64(img_file):
                return f"data:image/jpeg;base64,{base64.b64encode(img_file.getvalue()).decode()}"
            
            persona_url = img_to_base64(usuario)
            prenda_url = img_to_base64(prenda)
            
        except Exception as e:
            st.error(f"Error preparando imágenes: {e}")
            st.stop()
    
    # Llamar al modelo
    with st.spinner("🤖 La IA está probando la prenda... (⏱️ 30-60 segundos)"):
        try:
            # Usar versión específica y estable de IDM-VTON
            # Modelo alternativo más confiable: "yisol/idm-vton" (sin hash) usa la última versión
            output = replicate.run(
                "yisol/idm-vton",  # Sin hash, toma la última estable
                input={
                    "human_img": persona_url,
                    "garm_img": prenda_url,
                    "garment_des": garment_type,  # Ahora específico
                    "is_checked": is_checked,    # Si la prenda ya tiene fondo removido
                }
            )
            
            # El output puede ser una lista de URLs o un solo objeto
            if output:
                if isinstance(output, list) and len(output) > 0:
                    resultado_url = output[0]
                elif isinstance(output, str):
                    resultado_url = output
                else:
                    resultado_url = output
                
                st.success("✅ ¡Prueba completada!")
                st.image(resultado_url, caption="🎯 Resultado: La prenda en ti", use_container_width=True)
                
                # Botón para descargar
                st.download_button(
                    label="📥 Descargar resultado",
                    data=requests.get(resultado_url).content,
                    file_name="probador_virtual.jpg",
                    mime="image/jpeg"
                )
            else:
                st.error("El modelo no devolvió ningún resultado.")
                
        except replicate.exceptions.ModelError as e:
            st.error(f"❌ Error del modelo: {e}")
            st.info("💡 Sugerencias:\n- Reintenta con mejor iluminación\n- Asegura fondo claro en tu foto\n- Prueba otro tipo de prenda")
        except Exception as e:
            st.error(f"❌ Error inesperado: {type(e).__name__}: {e}")
            st.info("🔧 Esto suele pasar por:\n- Formato de imagen no válido\n- La API de Replicate está ocupada\n- Las imágenes son muy grandes (recomiendo < 2MB)")
