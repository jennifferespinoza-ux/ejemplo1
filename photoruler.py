import streamlit as st
import numpy as np
from PIL import Image, ImageDraw

st.set_page_config(page_title="Regla Virtual - Medición de Trombosis", layout="wide")

st.title("📏 Medidor de Trombosis en Cola de Ratón con Regla Virtual")

# Subir imagen
uploaded_file = st.file_uploader("Sube una foto de la cola del ratón", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    img_width, img_height = image.size

    # Configuración de regla virtual
    st.sidebar.header("⚙️ Configuración de la regla")
    orientation = st.sidebar.radio("Orientación de la regla", ["Horizontal", "Vertical"])
    pos = st.sidebar.slider(
        "Posición de la regla",
        0,
        img_height if orientation == "Horizontal" else img_width,
        step=5,
    )

    # Dibujo de regla sobre imagen
    img_copy = image.copy()
    draw = ImageDraw.Draw(img_copy)

    if orientation == "Horizontal":
        draw.line([(0, pos), (img_width, pos)], fill="red", width=3)
    else:
        draw.line([(pos, 0), (pos, img_height)], fill="red", width=3)

    st.image(img_copy, caption="Imagen con regla virtual", use_container_width=True)

    st.subheader("📐 Calibración")
    st.markdown("Marca cuántos **cm o mm** corresponde una referencia real en la regla (ejemplo: una sección de 1 cm en la regla física).")

    ref_px = st.number_input("Tamaño de referencia en píxeles (mide sobre la regla virtual)", value=100)
    ref_real = st.number_input("Longitud real de esa referencia", value=10.0)
    unit = st.selectbox("Unidad", ["cm", "mm"])

    if ref_px > 0:
        px_per_unit = ref_px / ref_real
        st.write(f"✅ Escala calculada: **{px_per_unit:.2f} px por {unit}**")

    st.subheader("📏 Medición manual")
    st.markdown("Introduce los valores de inicio y fin (en píxeles sobre la regla)")

    total_px = st.number_input("Longitud total de la cola (px)", value=0)
    thromb_px = st.number_input("Longitud de la zona de trombosis (px)", value=0)

    if total_px > 0 and thromb_px > 0 and ref_px > 0:
        total_real = total_px / px_per_unit
        thromb_real = thromb_px / px_per_unit
        percent = (thromb_real / total_real) * 100 if total_real > 0 else 0

        st.success(f"📐 Cola total: {total_real:.2f} {unit}")
        st.success(f"🟣 Trombosis: {thromb_real:.2f} {unit}")
        st.success(f"✅ Porcentaje de trombosis: {percent:.2f}%")
