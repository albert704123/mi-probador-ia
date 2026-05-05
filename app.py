import streamlit as st
import replicate
import os
import requests
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

# Función para convertir imagen a base64
def img_to_base64(uploaded_file):
    return f"data:image/jpeg;base64,{base64.b64encode(uploaded_file.getvalue()).decode()}"

# Interfaz
col1, col2 = st.columns(2)

with col1:
    prenda = st.camera_input("📸 1. Foto de la Prenda")
    if prenda:
        st.image(prenda, caption="Prenda", width=150)

with col2:
    usuario = st.camera_input("📸 2. Tu Foto (cuerpo entero)")
    if usuario:
        st.image(usuario, caption="Tú", width=150)

# Botón principal
if st.button("✨ ¡VER RESULTADO!", type="primary"):
    # Verificar que ambas fotos existen
    if prenda is None or usuario is None:
        st.warning("⚠️ Toma ambas fotos primero")
        st.stop()
    
    # Mostrar spinner mientras procesa
    with st.spinner("🧠 La IA está probando la prenda... (30-60 segundos)"):
        try:
            # Convertir fotos a base64 URL
            st.info("📷 Preparando imágenes...")
            prenda_url = img_to_base64(prenda)
            usuario_url = img_to_base64(usuario)
            
            # Llamar al modelo OOTDiffusion
            st.info("🤖 Consultando IA...")
            output = replicate.run(
                "levihsu/ootdiffusion",
                input={
                    "model_type": "upper_body",
                    "garment_image": prenda_url,
                    "model_image": usuario_url,
                    "n_samples": 1,
                    "guidance_scale": 2.0,
                    "seed": 42,
                    "step": 30
                }
            )
            
            # Procesar el resultado
            if output:
                # El output puede ser una lista de URLs o un string
                if isinstance(output, list) and len(output) > 0:
                    resultado_url = output[0]
                elif isinstance(output, str):
                    resultado_url = output
                else:
                    resultado_url = output
                
                st.success("✅ ¡Prueba completada!")
                st.image(resultado_url, caption="🎯 Resultado final", use_container_width=True)
                
                # Botón de descarga
                try:
                    respuesta = requests.get(resultado_url)
                    if respuesta.status_code == 200:
                        st.download_button(
                            label="💾 Descargar imagen",
                            data=respuesta.content,
                            file_name="mi_look_virtual.jpg",
                            mime="image/jpeg"
                        )
                except Exception as e:
                    st.warning(f"Nota: No se pudo preparar descarga ({e})")
            else:
                st.error("El modelo no devolvió ningún resultado")
                
        except replicate.exceptions.ModelError as e:
            st.error(f"❌ Error del modelo: {e}")
            st.info("💡 El modelo puede estar saturado. Intenta nuevamente en unos segundos.")
        except Exception as e:
            st.error(f"❌ Error inesperado: {type(e).__name__}")
            st.info("🔧 Verifica:\n- Token de Replicate válido\n- Las fotos son claras\n- Conexión a internet")
