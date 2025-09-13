import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.set_page_config(page_title="Medición de Trombosis en Cola de Ratón", layout="centered")

st.title("📏 Medición de Trombosis en Cola de Ratón")

st.markdown("""
Sube una **foto de la cola del ratón**, calibra la escala con la regla y mide
la proporción de trombosis.
""")

# ==========================
# 1. Subir imagen
# ==========================
archivo = st.file_uploader("Subir imagen", type=["jpg", "jpeg", "png", "tif", "tiff"])

if archivo is not None:
    img_pil = Image.open(archivo).convert("RGB")
    img_array = np.array(img_pil)

    st.image(img_array, caption="Imagen cargada", use_column_width=True)

    st.markdown("### ⚖️ Calibración de escala")
    st.write("Dibuja una regla sobre la imagen para convertir píxeles a mm/cm.")

    # ==========================
    # 2. Escala manual
    # ==========================
    escala_pix = st.number_input("Longitud de la regla (en píxeles)", min_value=1.0, value=100.0, step=1.0)
    escala_real = st.number_input("Longitud real de la regla (en mm)", min_value=0.1, value=10.0, step=0.1)

    factor = escala_real / escala_pix  # mm por píxel
    st.write(f"📐 Factor de conversión: **{factor:.4f} mm/píxel**")

    st.markdown("### 🖊️ Medición de la cola")

    # ==========================
    # 3. Medición de longitudes
    # ==========================
    total_pix = st.number_input("Longitud total de la cola (en píxeles)", min_value=1.0, value=200.0, step=1.0)
    tromb_pix = st.number_input("Longitud de la zona trombosada (en píxeles)", min_value=0.0, value=50.0, step=1.0)

    # Convertir a mm
    total_mm = total_pix * factor
    tromb_mm = tromb_pix * factor

    if total_mm > 0:
        porcentaje = (tromb_mm / total_mm) * 100
    else:
        porcentaje = 0

    st.markdown("### 📊 Resultados")
    st.write(f"- Longitud total cola: **{total_mm:.2f} mm**")
    st.write(f"- Longitud trombosada: **{tromb_mm:.2f} mm**")
    st.write(f"- % Trombosis: **{porcentaje:.2f} %**")

    # ==========================
    # 4. Exportar resultados
    # ==========================
    resultados = f"""
    Resultados de medición:
    -----------------------
    Longitud total cola: {total_mm:.2f} mm
    Longitud trombosada: {tromb_mm:.2f} mm
    % Trombosis: {porcentaje:.2f} %
    """

    st.download_button(
        "📥 Descargar resultados",
        data=resultados,
        file_name="resultado_trombosis.txt"
    )
