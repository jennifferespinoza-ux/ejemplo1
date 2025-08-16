import os
import io
import random
import textwrap
from datetime import datetime

import streamlit as st

# Optional: visualization
try:
    import py3Dmol  # pip install py3Dmol
    HAS_PY3DMOL = True
except Exception:
    HAS_PY3DMOL = False

# ============================
# Helpers
# ============================
AMINO_SET = set("ARNDCEQGHILKMFPSTWYV")


def clean_sequence(seq: str) -> str:
    seq = seq.upper()
    # remove whitespace and non-letters
    seq = "".join([c for c in seq if c.isalpha()])
    return seq


def validate_sequence(seq: str) -> tuple[bool, str]:
    if not seq:
        return False, "La secuencia está vacía."
    if any(c not in AMINO_SET for c in seq):
        malos = sorted(set(c for c in seq if c not in AMINO_SET))
        return False, f"Caracteres inválidos: {', '.join(malos)}. Use el alfabeto estándar de 20 aa."
    if len(seq) < 10:
        return False, "Secuencia muy corta (mínimo recomendado: 10 aa)."
    if len(seq) > 1200:
        return False, "Secuencia demasiado larga para la demostración (máx. 1200 aa)."
    return True, "OK"


def mock_pdb_from_sequence(seq: str, seed: int | None = None) -> str:
    """Genera un PDB sintético (trazado CA) con forma helicoidal para visualizar la secuencia.
    No es una predicción real. Útil como 'placeholder' si no hay backend.
    """
    if seed is not None:
        random.seed(seed)
    # Parámetros de una hélice simple
    R = 5.0
    pitch = 1.5  # avance por residuo
    pdb_lines = ["HEADER    MOCK STRUCTURE GENERATED IN STREAMLIT"]
    pdb_lines.append(f"REMARK    LENGTH {len(seq)}")
    pdb_lines.append("REMARK    NOT AN ALPHAFOLD PREDICTION")
    resseq = 1
    atom_serial = 1
    theta = 0.0
    dtheta = 2 * 3.14159265 / 3.6  # ~3.6 aa/turn
    for aa in seq:
        x = R * (1.0 + 0.05 * (random.random() - 0.5)) * __import__('math').cos(theta)
        y = R * (1.0 + 0.05 * (random.random() - 0.5)) * __import__('math').sin(theta)
        z = pitch * resseq + random.uniform(-0.2, 0.2)
        pdb_lines.append(
            f"ATOM  {atom_serial:5d}  CA  ALA A{resseq:4d}    {x:8.3f}{y:8.3f}{z:8.3f}  1.00 30.00           C"
        )
        atom_serial += 1
        theta += dtheta
        resseq += 1
    pdb_lines.append("TER")
    pdb_lines.append("END")
    return "\n".join(pdb_lines)


def call_alphafold_rest(seq: str, seed: int | None = None) -> str:
    """Ejemplo de conector REST.
    Espera que exista la variable ALPHAFOLD_API_URL que acepte POST {sequence, seed} y devuelva {'pdb': '...'}.
    """
    import requests  # local import para que sea opcional

    api_url = os.getenv("ALPHAFOLD_API_URL")
    api_token = os.getenv("ALPHAFOLD_API_TOKEN")
    if not api_url:
        raise RuntimeError(
            "No se encontró ALPHAFOLD_API_URL. Configure la URL del servicio (p. ej., ColabFold API)."
        )
    headers = {"Content-Type": "application/json"}
    if api_token:
        headers["Authorization"] = f"Bearer {api_token}"
    payload = {"sequence": seq}
    if seed is not None:
        payload["seed"] = int(seed)
    r = requests.post(api_url, json=payload, headers=headers, timeout=1800)
    r.raise_for_status()
    data = r.json()
    if "pdb" not in data:
        raise RuntimeError("La respuesta del servicio no contiene el campo 'pdb'.")
    return data["pdb"]


def predict_structure(seq: str, backend: str, seed: int | None = None) -> str:
    if backend == "Mock (demo)":
        return mock_pdb_from_sequence(seq, seed)
    elif backend == "AlphaFold/ColabFold (REST)":
        return call_alphafold_rest(seq, seed)
    else:
        raise ValueError("Backend no soportado")


def show_3d_view(pdb_text: str):
    if not HAS_PY3DMOL:
        st.info(
            "Instala 'py3Dmol' para visualizar estructuras en 3D (pip install py3Dmol). Se mostrará el PDB como texto.")
        st.code(pdb_text[:2000] + ("\n..." if len(pdb_text) > 2000 else ""), language="pdb")
        return
    view = py3Dmol.view(width=800, height=600)
    view.addModel(pdb_text, "pdb")
    # Estilos: intentar cartoon, si no, líneas
    view.setStyle({"cartoon": {}})
    view.addStyle({}, {"stick": {"radius": 0.2}})
    view.zoomTo()
    view.show()


# ============================
# UI
# ============================
st.set_page_config(page_title="Protein 3D Builder", page_icon="🧬", layout="wide")

# Sidebar (instrucciones)
st.sidebar.title("📘 Instrucciones")
st.sidebar.markdown(
    """
**Objetivo:** Generar/visualizar estructuras tridimensionales a partir de una secuencia de aminoácidos.

**Cómo usar**
1. Pegue su **secuencia** (solo letras *ACDEFGHIKLMNPQRSTVWY*).
2. Elija el **backend**:
   - *Mock (demo)*: genera una estructura sintética para probar la interfaz.
   - *AlphaFold/ColabFold (REST)*: requiere un servicio externo que reciba una secuencia y devuelva un PDB.
3. Presione **Run** para generar la estructura.
4. Use **Nueva estructura** para cambiar la semilla aleatoria y generar una variante.
5. Descargue el archivo **.pdb** si lo desea.

**Conectar a AlphaFold/ColabFold**
- Configure variables de entorno antes de ejecutar:
  - `ALPHAFOLD_API_URL` (ej.: endpoint de ColabFold/AlphaFold-API que devuelva JSON con `pdb`)
  - `ALPHAFOLD_API_TOKEN` (opcional)
- El app hará un `POST` con `{sequence, seed}` y espera un campo `pdb` en la respuesta.

**Notas**
- Este demo no ejecuta AlphaFold localmente (requerimientos computacionales altos).
- Para despliegue desde GitHub: incluya `requirements.txt` con `streamlit` y `py3Dmol`.
    """
)

# Main
st.title("🧬 Generador de Estructuras 3D de Proteínas")
st.caption("Ingrese una secuencia y genere/visualice su estructura (demo o AlphaFold REST)")

# Estado
if "seed" not in st.session_state:
    st.session_state.seed = int(datetime.utcnow().timestamp()) % 10_000_000
if "last_pdb" not in st.session_state:
    st.session_state.last_pdb = None
if "last_seq" not in st.session_state:
    st.session_state.last_seq = None

# Entrada de secuencia
example_seq = (
    "MGSSHHHHHHSSGLVPRGSHMSEQNNTEMTFQIQRIYTKDISFEAPNAPHVFQKDWLDNGSNQV"
)
seq_input = st.text_area(
    "Secuencia de aminoácidos (1 letra)",
    value=example_seq,
    height=140,
    help="Solo use letras del alfabeto estándar de 20 aa."
)
backend = st.selectbox(
    "Backend de predicción",
    ["Mock (demo)", "AlphaFold/ColabFold (REST)"]
)
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    run_clicked = st.button("▶️ Run", use_container_width=True)
with col2:
    new_clicked = st.button("🆕 Nueva estructura", use_container_width=True)
with col3:
    seed = st.number_input("Semilla aleatoria", min_value=0, max_value=2_147_483_647, value=st.session_state.seed)

# Lógica de botones
if new_clicked:
    st.session_state.seed = random.randint(0, 2_147_483_647)
    seed = st.session_state.seed
    run_clicked = True  # dispara una nueva corrida

if run_clicked:
    seq = clean_sequence(seq_input)
    ok, msg = validate_sequence(seq)
    if not ok:
        st.error(msg)
    else:
        with st.spinner("Generando estructura..."):
            try:
                pdb_text = predict_structure(seq, backend, seed)
                st.session_state.last_pdb = pdb_text
                st.session_state.last_seq = seq
            except Exception as e:
                st.error(f"Error al generar estructura: {e}")

# Visualización / descarga
if st.session_state.last_pdb:
    st.subheader("Vista 3D")
    show_3d_view(st.session_state.last_pdb)

    st.download_button(
        "💾 Descargar PDB",
        data=st.session_state.last_pdb,
        file_name=f"structure_{seed}.pdb",
        mime="chemical/x-pdb",
    )

    with st.expander("Ver PDB (texto)"):
        st.code(st.session_state.last_pdb[:5000] + ("\n..." if len(st.session_state.last_pdb) > 5000 else ""), language="pdb")

# Pie de página
st.caption("Este software se proporciona con fines educativos. AlphaFold es una marca de sus respectivos titulares.")
