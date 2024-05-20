import os
import cv2

def generate_timelapse(path, file_name):
    # Ruta de la carpeta con las imágenes
    imagen_path = f"../img/{path}"

    # Obtener la lista de archivos de imagen en la carpeta
    imagenes =  os.listdir(imagen_path)

    # Ordenar los archivos de imagen por nombre
    imagenes = sorted(imagenes, key=lambda x: os.path.getmtime(os.path.join(imagen_path, x)))
    
    # Obtener las dimensiones de la primera imagen
    primer_imagen = cv2.imread(os.path.join(imagen_path, imagenes[0]))
    altura, ancho, _ = primer_imagen.shape

    duration = 20
    num_fotogramas = len(imagenes)
    fps = num_fotogramas / duration

    # Crear el video de salida
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(f"../videos/{file_name}.mp4", fourcc, fps, (ancho, altura))
    
    # Procesar cada imagen y agregarla al video
    for imagen_file in imagenes:
        imagen = cv2.imread(os.path.join(imagen_path, imagen_file))
        video.write(imagen)

    # Liberar los recursos del video
    video.release()