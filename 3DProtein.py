# 3DProtein.py

import streamlit as st
import random
import py3Dmol

# Diccionario de conversión de tres letras a una letra
amino_dict = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C",
    "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I",
    "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P",
    "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V"
}

# Función de conversión
def convertir_tres_a_una(seq_tres):
    secuencia = seq_tres.upper().split()
    return ''.join([amino_dict.get(res, 'X') for res in secuencia])

# Configuración de la interfaz
st.sidebar.title("🧬 Instrucciones")
st.sidebar.write("1. Si tienes secuencia en 3 letras, conviértela primero.\n"
                 "2. Ingresa la secuencia en letras simples (A, R, N, etc.).\n"
                 "3. Haz clic en **Run** para ver la estructura.\n"
                 "4. Usa **Nueva estructura** para generar otra visualización.")

st.title("Generador de estructuras 3D de proteínas")

# Conversión 3 letras -> 1 letra
st.subheader("Conversión de 3 letras a 1 letra")
entrada_tres = st.text_area("Introduce la secuencia en formato de 3 letras (separadas por espacio)")
if st.button("Convertir a 1 letra"):
    resultado = convertir_tres_a_una(entrada_tres)
    st.success(f"Secuencia convertida: {resultado}")

# Entrada de secuencia
st.subheader("Generación de estructura 3D")
seq_input = st.text_area("Introduce la secuencia de aminoácidos en formato de 1 letra")

# Botones
col1, col2 = st.columns(2)
run = col1.button("Run")
new_structure = col2.button("Nueva estructura")

# Función para simular una estructura PDB de ejemplo
def generar_pdb(seq):
    pdb = "HEADER    MOCK PROTEIN\n"
    for i, aa in enumerate(seq, start=1):
        x, y, z = random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10)
        pdb += f"ATOM  {i:5d}  CA  {aa}   {i:4d}    {x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           C\n"
    pdb += "END\n"
    return pdb

# Visualización con py3Dmol
if run or new_structure:
    if seq_input:
        pdb_data = generar_pdb(seq_input)
        view = py3Dmol.view(width=500, height=400)
        view.addModel(pdb_data, 'pdb')
        view.setStyle({'cartoon': {'color': 'spectrum'}})
        view.zoomTo()
        view_html = view._make_html()
        st.components.v1.html(view_html, height=400)
        st.download_button("Descargar PDB", pdb_data, file_name="estructura.pdb")
    else:
        st.warning("⚠️ Ingresa una secuencia primero.")
