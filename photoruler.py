import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

st.set_page_config(page_title="Regla Virtual Rotable", layout="wide")

st.title("📏 Regla Virtual Rotable para medir trombosis en cola de ratón")

uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")  # 👈 usar PIL directamente

    st.write("👉 Usa el mouse para **arrastrar, escalar o rotar la regla** sobre la cola")

    # Canvas interactivo
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=2,
        stroke_color="#FF0000",
        background_image=image,  # 👈 PIL.Image sí funciona
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="transform",
        initial_drawing={
            "version": "4.4.0",
            "objects": [
                {
                    "type": "rect",
                    "left": 50,
                    "top": 50,
                    "width": 300,
                    "height": 20,
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
    if canvas_result.json_data is not None and len(canvas_result.json_data["objects"]) > 0:
        try:
            obj = canvas_result.json_data["objects"][0]
            length_px = max(obj["width"], obj["height"])
            length_real = length_px / px_per_unit
            st.success(f"Longitud medida: {length_real:.2f} cm (≈ {length_px:.0f} px)")
        except Exception as e:
            st.warning(f"No se pudo calcular: {e}")
