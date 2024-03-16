import streamlit as st
import pandas as pd
from fuzzywuzzy import process

textos_entrada = ['tomate', 'limones', 'mandarinas', 'manzanas', 'plátano']

def filtrar_filas_por_similitud(dataframe, texto, columna):
    mejor_puntaje = 0
    mejor_fila = None
    
    # Iterar sobre las filas del DataFrame
    for index, fila in dataframe.iterrows():
        texto_fila = fila[columna]
        puntaje_similitud = process.extractOne(texto_fila, [texto])[1]
        # Actualizar la mejor fila si se encuentra un puntaje de similitud más alto
        if puntaje_similitud > mejor_puntaje:
            mejor_puntaje = puntaje_similitud
            mejor_fila = fila    
    return mejor_fila


def main():
    
    # Usa la base de datos de alimentos
    df = pd.read_csv('../../data/interim/alcampo_scraped.csv')
    
    frutitas = '../../data/processed/frutitas.csv'
    
    for i in textos_entrada:
        filtrar_filas_por_similitud(df, i,'nombre')
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
    