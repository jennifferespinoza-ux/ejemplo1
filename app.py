import streamlit as st

def resolver_ecuacion(a: float, b: float):
    if a == 0:
        if b == 0:
            return "La ecuación tiene infinitas soluciones."
        else:
            return "La ecuación no tiene solución."
    else:
        x = -b / a
        return f"La solución es: x = {x:.4f}"

# Interfaz en Streamlit
st.title("Resolución de Ecuaciones de Primer Grado")
st.write("Ecuaciones de la forma **ax + b = 0**")

# Entrada de coeficientes
a = st.number_input("Ingrese el valor de a:", value=1.0)
b = st.number_input("Ingrese el valor de b:", value=0.0)

if st.button("Resolver"):
    resultado = resolver_ecuacion(a, b)
    st.success(resultado)
