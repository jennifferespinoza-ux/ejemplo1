import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image

st.set_page_config(page_title="Regla Virtual - Medición Trombosis", layout="wide")

st.title("📏 Regla Virtual para medir trombosis en colas de ratón")

# Subir imagen
uploaded_file = st.file_uploader("Sube una foto de la cola del ratón", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Abrir la imagen como PIL y convertir a RGBA
    image = Image.open(uploaded_file).convert("RGBA")

    # Mostrar la imagen original
    st.subheader("Imagen cargada")
    st.image(image, use_container_width=True)

    st.markdown("👉 Ahora puedes usar la **regla azul** en el canvas para medir la cola. "
                "Arrástrala, estírala o gírala con el cursor.")

    # Canvas interactivo (solo la regla, fondo transparente)
    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 255, 0.3)",  # color del rectángulo
        stroke_width=2,
        stroke_color="blue",
        background_color="rgba(0,0,0,0)",  # 👈 transparente
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

    st.subheader("📐 Calibración de la regla")
    px_per_unit = st.number_input(
        "¿Cuántos píxeles corresponden a 1 cm?",
        value=100,
        min_value=1
    )

    st.subheader("📏 Resultado de la medición")
    if canvas_result.json_data is not None and len(canvas_result.json_data["objects"]) > 0:
        try:
            obj = canvas_result.json_data["objects"][0]
            # Medimos la dimensión mayor (ancho o alto) según rotación
            length_px = max(obj["width"], obj["height"])
            length_real = length_px / px_per_unit
            st.success(f"Longitud medida: {length_real:.2f} cm (≈ {length_px:.0f} px)")
        except Exception as e:
            st.warning(f"No se pudo calcular: {e}")

