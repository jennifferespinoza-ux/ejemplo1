import streamlit as st
import py3Dmol

st.set_page_config(layout="wide")

# Barra lateral con instrucciones
st.sidebar.title("Instrucciones")
st.sidebar.markdown("""
1. Si tienes una secuencia en **tres letras**, conviértela primero a una letra.
2. Ingresa una secuencia de aminoácidos (en una letra).
3. Presiona **Run** para generar la estructura.
4. Presiona **Nueva estructura** para reiniciar.
""")

# Conversión de tres letras a una letra
three_to_one = {
    'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C',
    'GLN':'Q','GLU':'E','GLY':'G','HIS':'H','ILE':'I',
    'LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P',
    'SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'
}

st.header("Generador 3D de Proteínas")

convert_option = st.checkbox("Convertir secuencia de 3 letras a 1 letra")
seq_input = st.text_area("Ingresa tu secuencia:")

if convert_option and seq_input:
    parts = seq_input.strip().split()
    seq_converted = ''.join([three_to_one.get(res.upper(), 'X') for res in parts])
    st.write("**Secuencia convertida:**", seq_converted)
    sequence = seq_converted
else:
    sequence = seq_input.strip().upper()

# Botones
col1, col2 = st.columns(2)
run = col1.button("Run")
reset = col2.button("Nueva estructura")

# Función para generar un PDB ficticio a partir de la secuencia
def generate_fake_pdb(seq):
    pdb_lines = []
    for i, aa in enumerate(seq, start=1):
        x, y, z = i*1.5, 0.0, 0.0
        pdb_lines.append(f"ATOM  {i:5d}  CA  {aa} A{i:4d}    {x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           C")
    pdb_lines.append("TER")
    pdb_lines.append("END")
    return "\n".join(pdb_lines)

# Función para mostrar visualización en Streamlit
def show_structure(pdb_data, width=600, height=400):
    viewer = py3Dmol.view(width=width, height=height)
    viewer.addModel(pdb_data, "pdb")
    viewer.setStyle({"cartoon": {"color": "spectrum"}})
    viewer.zoomTo()
    return viewer._make_html()

# Mostrar estructura si se presiona Run
if run and sequence:
    pdb_data = generate_fake_pdb(sequence)
    html_viewer = show_structure(pdb_data)
    st.components.v1.html(html_viewer, height=500, width=700, scrolling=False)

    # Botón para descargar PDB
    st.download_button(
        label="Descargar PDB",
        data=pdb_data,
        file_name="estructura.pdb",
        mime="chemical/x-pdb"
    )

# Ejemplo automático al inicio (1CRN desde RCSB)
if not sequence and not run:
    st.subheader("Ejemplo: Proteína 1CRN")
    viewer = py3Dmol.view(query='pdb:1CRN', width=600, height=400)
    viewer.setStyle({"cartoon": {"color": "spectrum"}})
    viewer.zoomTo()
    html_viewer = viewer._make_html()
    st.components.v1.html(html_viewer, height=500, width=700, scrolling=False)
