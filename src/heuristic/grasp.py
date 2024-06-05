import random
import math

def grasp(distance_matrix, city, alpha=0.5):
    """
    Implementación del algoritmo GRASP para el problema del agente viajero (TSP).

    Parámetros:
    -----------
    distance_matrix ([[int/float]]): Matriz de distancias entre los nodos del problema.
    city (list): Lista de nombres o identificadores de las ciudades o nodos.
    max_iterations (int): Número máximo de iteraciones de GRASP.
    alpha (float): Parámetro que controla la aleatoriedad de la construcción voraz (0 <= alpha <= 1).
    show_iterations (bool): Si True, muestra las iteraciones de la búsqueda local.

    Retorna:
    --------
    tuple: Una tupla que contiene:
           - distancia_total (int/float): La distancia total de la mejor ruta encontrada.
           - tour (list): La mejor ruta (lista de nodos) encontrada.
    """
    
    best_distance = float('inf')
    best_tour = None
    max_iterations= 50
    
    for _ in range(max_iterations):
        # Construcción voraz aleatorizada
        distance, tour = greedy_randomized_construction(distance_matrix, city, alpha)
        
        # Búsqueda local (2-opt)
        current_distance, current_tour = local_search(distance_matrix, distance, tour)
        
        # Actualizar la mejor solución encontrada
        if current_distance < best_distance:
            best_distance = current_distance
            best_tour = current_tour
    
    return best_distance, best_tour

def greedy_randomized_construction(distance_matrix, city, alpha):
    """
    Construcción voraz aleatorizada para generar una solución inicial.

    Parámetros:
    -----------
    distance_matrix ([[int/float]]): Matriz de distancias entre los nodos del problema.
    city (list): Lista de nombres o identificadores de las ciudades o nodos.
    alpha (float): Parámetro que controla la aleatoriedad de la construcción voraz (0 <= alpha <= 1).

    Retorna:
    --------
    list: La solución inicial (ruta) construida.
    """
    
    n = len(distance_matrix)

    remaining_cities = [i for i in range(1, n)] # Lista de ciudades restantes
    tour = [0]  # Inicializar la ruta con la primera ciudad

    while remaining_cities:
        # print(remaining_cities)
        candidate_list = restricted_candidate_list(distance_matrix, city, tour[-1], remaining_cities, alpha)
        next_city = random.choice(candidate_list)
        tour.append(next_city)
        remaining_cities.remove(next_city)
    tour.append(0)
    distancia_total = sum(distance_matrix[tour[i]][tour[i + 1]] for i in range(n))
    
    return distancia_total, tour

def restricted_candidate_list(distance_matrix, city, current_index, remaining_cities, alpha):
    """
    Construye la lista restringida de candidatos (RCL) para la construcción voraz aleatorizada.

    Parámetros:
    -----------
    distance_matrix ([[int/float]]): Matriz de distancias entre los nodos del problema.
    current_city (str): La ciudad actual en la ruta.
    remaining_cities (list): Lista de ciudades restantes por visitar.
    alpha (float): Parámetro que controla la aleatoriedad de la construcción voraz (0 <= alpha <= 1).

    Retorna:
    --------
    list: La lista restringida de candidatos (RCL).
    """
    
    n = len(distance_matrix)

    distances = [0] * n 
    for c in remaining_cities:
        distances[c] = distance_matrix[current_index][c] 

    min_distance = min([d for d in distances if d != 0])
    max_distance = max(distances)
    # print(remaining_cities)
    bias = min_distance + alpha * (max_distance - min_distance)

    rcl = []

    for i, d in enumerate(distances):
        if d <= bias and d != 0:
            rcl.append(i)

    return rcl

def local_search(distance_matrix, distance, tour):

    n = len(distance_matrix)
   
    improved = True
    itr = 0
    while improved:

        improved = False
        for i in range(n):
            for j in range(i + 1, n):
                # Obtener los dos bordes actuales de la ruta
                cur1 = (tour[i], tour[(i + 1) % n])
                cur2 = (tour[j], tour[(j + 1) % n])
                cur_length = (
                    distance_matrix[tour[i]][tour[(i + 1) % n]]
                    + distance_matrix[tour[j]][tour[(j + 1) % n]]
                )

                # Obtener los dos 'nuevos' bordes para la ruta
                new1 = (tour[i], tour[j])
                new2 = (tour[(i + 1) % n], tour[(j + 1) % n])
                new_length = (
                    distance_matrix[tour[i]][tour[j]]
                    + distance_matrix[tour[(i + 1) % n]][tour[(j + 1) % n]]
                )

                # Actualizar la ruta, si se mejora
                if new_length < cur_length:
                    # print(f"Intercambiando bordes {cur1} y {cur2} por {new1} y {new2}")
                    tour[i + 1 : j + 1] = tour[i + 1 : j + 1][::-1]
                    improved = True

                itr += 1
    # Calcular la distancia total de la ruta
    distancia_total = sum(distance_matrix[tour[i]][tour[i + 1]] for i in range(n))

    return distancia_total, tour
