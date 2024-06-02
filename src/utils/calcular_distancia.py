import math


# Utilidad para calcular la matriz de distancias entre las ciudades.
# Recibe una matriz con las coordenadas de las ciudades.
def calcular_distancia(cities):
    distance_matrix = [
        [
            math.sqrt(
                (start_city[0] - end_city[0]) ** 2 + (start_city[1] - end_city[1]) ** 2
            )
            for end_city in cities
        ]
        for start_city in cities
    ]
    return distance_matrix


def calcular_costo_ruta(ruta, distances):
    distance = sum(distances[ruta[i - 1]][ruta[i]] for i in range(len(distances) + 1))
    return distance

def calculate_total_distance(tour, distance_matrix):
    """
    Calcula la distancia total de un recorrido.
    """
    total_distance = 0
    for i in range(len(tour)):
        # Agrega la distancia entre la actual ciudad y la siguiente ciudad
        total_distance += distance_matrix[tour[i]][tour[(i + 1) % len(tour)]]
    return total_distance
