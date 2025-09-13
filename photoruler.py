import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

st.set_page_config(page_title="Regla Virtual Rotable", layout="wide")

st.title("📏 Regla Virtual Rotable para medir trombosis en cola de ratón")

uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    st.write("👉 Usa el mouse para **arrastrar, escalar o rotar la regla** sobre la cola")

    # Cargar una regla de referencia (puedes reemplazar con tu propia imagen de regla en PNG transparente)
    rule_img = Image.new("RGBA", (300, 20), (255, 0, 0, 120))  # regla rectangular roja básica

    # Canvas interactivo
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # color de relleno de los shapes
        stroke_width=2,
        stroke_color="#FF0000",
        background_image=image,
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="transform",  # permite mover/rotar/escala objetos
        initial_drawing={
            "version": "4.4.0",
            "objects": [
                {
                    "type": "rect",
                    "left": 50,
                    "top": 50,
                    "width": rule_img.width,
                    "height": rule_img.height,
                    "fill": "rgba(0,0,255,0.3)",
                    "stroke": "blue",
                    "strokeWidth": 2,
                    "angle": 0
                }
            ]
        },
        key="canvas",
    )

    st.subheader("📐 Medición")

    px_per_unit = st.number_input("Cuántos píxeles corresponden a 1 cm (calibración)", value=100)
    if canvas_result.json_data is not None:
        try:
            obj = canvas_result.json_data["objects"][0]
            length_px = obj["width"] if obj["width"] > obj["height"] else obj["height"]
            length_real = length_px / px_per_unit
            st.success(f"Longitud medida: {length_real:.2f} cm (≈ {length_px:.0f} px)")
        except Exception as e:
            st.warning("Mueve la regla y luego calcula")

