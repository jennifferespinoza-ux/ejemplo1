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
                 "4. Usa **Nueva estructura** para generar otra visualización.\n"
                 "5. Descarga el archivo en formato PDB o TXT según prefieras.\n"
                 "6. También puedes cargar una proteína real desde la base de datos PDB (RCSB).")

st.title("Generador de estructuras 3D de proteínas")

# Conversión 3 letras -> 1 letra
st.subheader("Conversión de 3 letras a 1 letra")
entrada_tres = st.text_area("Introduce la secuencia en formato de 3 letras (separadas por espacio)")
if st.button("Convertir a 1 letra"):
    resultado = convertir_tres_a_una(entrada_tres)
    st.success(f"Secuencia convertida: {resultado}")

# Entrada de secuencia
st.subheader("Generación de estructura 3D desde secuencia")
seq_input = st.text_area("Introduce la secuencia de aminoácidos en formato de 1 letra")

# Ejemplo de secuencia
if st.checkbox("Usar ejemplo de secuencia (proteína corta)"):
    seq_input = "ACDEFGHIKLMNPQRSTVWY"  # un ejemplo con los 20 aminoácidos estándar
    st.info(f"Ejemplo cargado: {seq_input}")

# Entrada para cargar directamente un código PDB real
def cargar_pdb(pdb_id):
    view = py3Dmol.view(query=f"pdb:{pdb_id}", width=600, height=500)
    view.setStyle({'cartoon': {'color': 'spectrum'}})
    view.zoomTo()
    return view

st.subheader("Visualizar proteína desde el RCSB PDB")
pdb_code = st.text_input("Introduce un código PDB (ejemplo: 1CRN, 4HHB, etc.)", value="1CRN")
if st.button("Cargar PDB real"):
    if pdb_code:
        view = cargar_pdb(pdb_code)
        html = view._make_html()
        st.components.v1.html(html, height=500, width=600)
        st.download_button("Descargar PDB desde RCSB", html, file_name=f"{pdb_code}.html")
    else:
        st.warning("⚠️ Ingresa un código PDB válido.")

# Botones para estructura simulada desde secuencia
col1, col2 = st.columns(2)
run = col1.button("Run")
new_structure = col2.button("Nueva estructura")

# Función para simular una estructura PDB de ejemplo
def generar_pdb(seq):
    pdb = "HEADER    MOCK PROTEIN\n"
    for i, aa in enumerate(seq, start=1):
        x, y, z = random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10)
        pdb += f"ATOM  {i:5d}  CA  ALA A{i:4d}    {x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           C\n"
    pdb += "TER\nEND\n"
    return pdb

# Visualización con py3Dmol desde secuencia
if run or new_structure:
    if seq_input:
        pdb_data = generar_pdb(seq_input)
        view = py3Dmol.view(width=600, height=500)
        view.addModel(pdb_data, 'pdb')
        view.setStyle({'cartoon': {'color': 'spectrum'}})
        view.zoomTo()
        st.components.v1.html(view._make_html(), height=500, width=600)

        # Botones de descarga
        st.download_button("Descargar PDB generado", pdb_data, file_name="estructura.pdb")
        st.download_button("Descargar Secuencia TXT", seq_input, file_name="secuencia.txt")
    else:
        st.warning("⚠️ Ingresa una secuencia primero.")

# Mostrar ejemplo por defecto automáticamente
st.subheader("Ejemplo automático")
st.write("Visualización automática del código PDB **1CRN** para comprobar la app:")
default_view = cargar_pdb("1CRN")
st.components.v1.html(default_view._make_html(), height=500, width=600)
