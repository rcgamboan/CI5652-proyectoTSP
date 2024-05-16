
# Función que lee un archivo .tsp y devuelve una matriz con las coordenadas de los nodos
# Se ignoran las primeras 6 lineas del archivo que contienen informacion respecto al problema
def obtener_ciudades(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    start_index = lines.index('NODE_COORD_SECTION\n') + 1

    # Lee las lineas desde la 7 a la penúltima, donde se encuentran las coordendas de los nodos
    node_lines = lines[start_index:-1]

    # Inicializa la matriz de coordenadas
    coordinates = []

    # Procesa cada línea
    for line in node_lines:
        # Divide la línea en palabras
        words = line.split()

        # Convierte las coordenadas a flotantes y las añade a la matriz
        coordinates.append([float(words[1]), float(words[2])])

    return coordinates

# Funcion para obtener la mejor ruta de los archivos .opt.tour
# para luego calcular la distancia, ya que los archivos no la incluyen
# se les resta 1 a las ciudades para que coincidan con el indice de la matriz
def obtener_mejor_ruta(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    start_index = lines.index('TOUR_SECTION\n') + 1
    end_index = lines.index('-1\n')
    node_lines = lines[start_index:end_index]
    ruta = []
    # Procesa cada línea
    for line in node_lines:
        # Divide la línea en palabras
        words = line.split()
        for num in words:
            ruta.append(int(num)-1)

        # Convierte las coordenadas a flotantes y las añade a la matriz
        #ruta.append(int(words[0])-1)
    ruta.append(ruta[0])
    return ruta