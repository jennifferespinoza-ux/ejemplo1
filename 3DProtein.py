import streamlit as st
import py3Dmol
import random

# Diccionario de conversión de tres letras a una letra
amino_dict = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C",
    "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I",
    "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P",
    "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V"
}

# Función de conversión
def convertir_tres_a_una(seq_tres):
    partes = seq_tres.strip().upper().split()
    return "".join(amino_dict.get(res, "X") for res in partes)

# Función simulada para generar estructura PDB desde secuencia
def generar_estructura_pdb(seq: str, seed: int = None):
    if not seed:
        seed = random.randint(1, 10000)
    # Aquí deberías conectar con AlphaFold/ColabFold para obtener la estructura real
    # Por ahora devolvemos un modelo PDB ficticio
    pdb_mock = f"""
HETATM    1  N   ALA A   1      {seed%10+10}.000  11.000   8.000  1.00 20.00           N
HETATM    2  CA  ALA A   1      {seed%5+12}.000  12.000   8.000  1.00 20.00           C
HETATM    3  C   ALA A   1      {seed%7+13}.000  13.000   9.000  1.00 20.00           C
HETATM    4  O   ALA A   1      {seed%3+14}.000  14.000   9.500  1.00 20.00           O
END
"""
    return pdb_mock

# Barra lateral con instrucciones
st.sidebar.title("📘 Instrucciones")
st.sidebar.write("""
1. Puede ingresar una secuencia en formato **tres letras** (ejemplo: ALA GLY SER) y convertirla a una letra.
2. Ingrese una **secuencia de aminoácidos** usando el alfabeto estándar (ACDEFGHIKLMNPQRSTVWY).
3. Presione **Run** para generar una estructura 3D.
4. Use el botón **Nueva estructura** para cambiar la semilla aleatoria y visualizar otra conformación.
5. Mueva la estructura con el mouse: clic izquierdo (rotar), clic derecho (mover), rueda (zoom).
""")

# Interfaz principal
st.title("Generación de Estructuras de Proteínas 🧬")

# Conversión de tres letras a una letra
st.subheader("Conversión de secuencia (tres letras → una letra)")
seq_tres = st.text_area("Ingrese la secuencia en tres letras (ejemplo: ALA GLY SER):", value="")
if st.button("Convertir a una letra"):
    seq_convertida = convertir_tres_a_una(seq_tres)
    st.success(f"Secuencia convertida: {seq_convertida}")
    st.session_state["secuencia_convertida"] = seq_convertida

# Secuencia de prueba cargada por defecto
secuencia = st.text_area("Ingrese la secuencia de aminoácidos:",
                         value=st.session_state.get("secuencia_convertida", "ACDEFGHIKLMNPQRSTVWY"),
                         height=100)

# Botones
col1, col2 = st.columns(2)

if "estructura" not in st.session_state:
    st.session_state.estructura = None
    st.session_state.seed = None

if col1.button("Run"):
    st.session_state.seed = random.randint(1, 10000)
    st.session_state.estructura = generar_estructura_pdb(secuencia, st.session_state.seed)

if col2.button("Nueva estructura"):
    st.session_state.seed = random.randint(1, 10000)
    st.session_state.estructura = generar_estructura_pdb(secuencia, st.session_state.seed)

# Visualización 3D en la misma página
if st.session_state.estructura:
    st.subheader("Visualización 3D de la proteína")
    viewer = py3Dmol.view(width=500, height=400)
    viewer.addModel(st.session_state.estructura, "pdb")
    viewer.setStyle({"cartoon": {"color": "spectrum"}})
    viewer.zoomTo()
    viewer.show()
    
    # Render en Streamlit
    viewer_html = viewer._make_html()
    st.components.v1.html(viewer_html, height=500, width=700, scrolling=False)
    
    # Opción de descarga
    st.download_button("Descargar PDB", data=st.session_state.estructura, file_name="estructura.pdb")
