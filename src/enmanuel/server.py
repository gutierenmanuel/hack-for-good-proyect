from flask import Flask, request
import os


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
    
    return '¡Imagen recibida y guardada con éxito!', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)