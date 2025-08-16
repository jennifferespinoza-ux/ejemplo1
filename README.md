# Generador de estructuras 3D de proteínas 🧬

Esta aplicación permite:
- Convertir secuencias de aminoácidos de **tres letras → una letra**.
- Ingresar secuencias en formato de una letra.
- Generar estructuras 3D simuladas.
- Visualizar la proteína en la misma página.
- Descargar el archivo PDB generado.

## Instrucciones
1. Abrir la aplicación en Streamlit.
2. Ingresar secuencia en tres letras o directamente en una letra.
3. Presionar **Run** para generar una estructura.
4. Usar **Nueva estructura** para obtener una variante diferente.
5. Rotar y acercar la estructura con el mouse.

## Instalación local
```bash
pip install -r requirements.txt
streamlit run 3DProtein.py
