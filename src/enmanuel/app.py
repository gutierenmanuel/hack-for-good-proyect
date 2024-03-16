import scrapgpt as gpt
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import cv2

from flask import Flask, request
import os


driver = gpt.open_driver()

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'  # Carpeta donde se guardarán las imágenes

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return 'No se encontró ninguna imagen en la solicitud', 400
    
    image_file = request.files['image']
    
    # Guardar la imagen en la carpeta de carga con el nombre ticket.jpg
    image_path = os.path.join(UPLOAD_FOLDER, 'ticket.jpg')
    image_file.save(image_path)
    
    print('¡Imagen recibida y guardada con éxito en {}!'.format(image_path))
    
    img = Image.open(image_path)

    ruta_de_la_imagen = 'uploads/ticket.jpg'

    img.save('temp.png')
    # Cargar la imagen
    imagen = cv2.imread(ruta_de_la_imagen)

    # Aumentar el contraste
    alpha = 1.7  # Factor de contraste
    beta = 0.2     # Sesgo de brillo
    imagen_contrastada = cv2.convertScaleAbs(imagen, alpha=alpha, beta=beta)

    # Convertir a escala de grises
    gris = cv2.cvtColor(imagen_contrastada, cv2.COLOR_BGR2GRAY)

    # Aplicar umbral adaptativo
    umbral_adaptativo = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Aplicar filtro de mediana para eliminar ruido
    filtrada = cv2.medianBlur(umbral_adaptativo, 3)

    # Guardar la imagen binarizada adaptativa
    cv2.imwrite('imagen_binarizada_adaptativa.jpg', umbral_adaptativo)

    # Usar Tesseract para extraer texto de la imagen binarizada adaptativa
    texto_extraido = pytesseract.image_to_string(Image.open('imagen_binarizada_adaptativa.jpg'), lang='spa')

    texto = repr(texto_extraido)

    respuesta = gpt.scrap_gpt(driver, f'dime sin ningun comentario tuyo, que de todo este texto solo la lista de alimentos:{texto}')

    with open('../../data/processed/alimentos.txt', 'w') as archivo:
        # Escribir el contenido de la variable en el archivo
        archivo.write(respuesta)

    print(respuesta)

    receta = gpt.scrap_gpt(driver, f'ahora dime una posible receta con algunos de esos ingredientes')

    with open('../../data/processed/receta.txt', 'w') as archivo:
        # Escribir el contenido de la variable en el archivo
        archivo.write(receta)

    print(receta)

    return '¡Imagen recibida y guardada con éxito!', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)
