import streamlit as st
import pandas as pd

def main():
    # Usa la base de datos de alimentos
    df = pd.read_csv('../../data/interim/alcampo_scraped.csv')

    # Crear la tabla HTML
    html_table = "<table><tr><th>Imagen</th><th>Nombre</th><th>Durabilidad</th></tr>"
    for index, row in df.head().iterrows():
        html_table += f"<tr><td>{row['Imagen']}</td><td>{row['nombre']}</td><td>{row['Durabilidad']}</td></tr>"
    html_table += "</table>"

    # Mostrar la tabla HTML
    st.write("Productos:")
    st.markdown(html_table, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    