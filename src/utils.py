import os
import requests
from urllib.parse import urlparse
import pandas as pd
import dataframe_image as dfi
import seaborn as sns
import matplotlib.pyplot as plt
import math

def descargar_archivo(url, carpeta_local='',nombre=None):
    try:

        # Obtener el nombre del archivo de la URL
        nombre_archivo = os.path.basename(urlparse(url).path)

        # Combinar la carpeta local y el nombre del archivo para obtener la ruta completa
        ruta_local = os.path.join(carpeta_local, nombre_archivo)

        # Verificar si el archivo ya existe
        if os.path.exists(ruta_local):
            print(f'El archivo {nombre_archivo} ya existe en la carpeta local.')
            ruta_local = os.path.join(carpeta_local, nombre)


        # Realizar la solicitud GET para descargar el archivo
        respuesta = requests.get(url)
        respuesta.raise_for_status()  # Verificar si la solicitud fue exitosa

        # Guardar el contenido en el archivo local
        with open(ruta_local, 'wb') as archivo_local:
            archivo_local.write(respuesta.content)

        print(f'Archivo descargado exitosamente en: {ruta_local}')

    except Exception as e:
        pass
    


## ---


def dataframe_to_image(dataframe,ruta_imagen):

    dfi.export(dataframe,ruta_imagen)


## ---



def plot_categorical_histograms(dataframe, max_columns=3):
    # Obtén la lista de columnas categóricas
    categorical_columns = dataframe.select_dtypes(include=['object']).columns.tolist()

    # Calcula el número total de variables categóricas y el número de filas y columnas deseadas
    num_categorical = len(categorical_columns)
    num_cols = min(num_categorical, max_columns)
    num_rows = math.ceil(num_categorical / num_cols)

    # Configura el tamaño del gráfico
    plt.figure(figsize=(5 * max_columns, 5 * num_rows))

    # Itera sobre las columnas categóricas y crea un histograma para cada una
    for i, column in enumerate(categorical_columns, start=1):
        plt.subplot(num_rows, num_cols, i)
        sns.histplot(data=dataframe, x=column)  # Puedes ajustar las opciones según tu preferencia
        plt.title(column)
        plt.xticks(rotation=45)
        plt.ylabel('Frecuencia')
        plt.xlabel('')


    # Ajusta el espaciado entre subgráficos
    plt.tight_layout()

    # Muestra el gráfico
    plt.show()


## --- 

import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np

def plot_numerical_data(dataframe):

    total_data = dataframe

    for column in dataframe.columns:

        fig, axis = plt.subplots(2, 1, figsize = (8,4), gridspec_kw={'height_ratios': [6, 1]})

        # Calcula la media de los datos
        media = np.mean(dataframe[column])
        mediana = np.median(dataframe[column])
        desviacion_estandar = np.std(dataframe[column])

        # Crear una figura múltiple con histogramas y diagramas de caja
        sns.histplot(ax = axis[0],
                    data = total_data,
                    kde=True,
                    x = column).set(xlabel = None)
        axis[0].axvline(media, color='red', linestyle='dashed', linewidth=1, label='Media')
        axis[0].axvline(mediana, color='orange', linestyle='dashed', linewidth=1, label='Mediana')
        axis[0].axvline(media + desviacion_estandar, color='green', linestyle='dashed', linewidth=1, label='Desviación Estándar')
        axis[0].axvline(media - desviacion_estandar, color='green', linestyle='dashed', linewidth=1)

        sns.boxplot(ax = axis[1], data = total_data, x = column).set(xlabel = None)
        axis[1].axvline(media, color='red', linestyle='dashed', linewidth=1, label='Media')
        axis[1].axvline(mediana, color='orange', linestyle='dashed', linewidth=1, label='Mediana')
        axis[1].axvline(media + desviacion_estandar, color='green', linestyle='dashed', linewidth=1)
        axis[1].axvline(media - desviacion_estandar, color='green', linestyle='dashed', linewidth=1)

        axis[0].legend()

        fig.suptitle(column)

        # Ajustar el layout
        plt.tight_layout()

        # Mostrar el plot
        plt.show()

#------

def ver_dataframe_completo():

    # Configura Pandas para mostrar DataFrames completos sin truncar
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_colwidth', None)

def ver_dataframe_columnas():

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)

def restaurar_ajuste():

    # Restaura el valor de pandas para mostrar dataframes truncados
    pd.reset_option('all')
    