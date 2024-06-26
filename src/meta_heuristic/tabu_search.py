import random
import math
from collections import deque
from heuristic.nearest_neighbour import nearest_neighbour
from heuristic.double_bridge import calculate_total_distance

def two_opt_swap(tour, i, j):
    new_tour = tour[:i] + tour[i:j+1][::-1] + tour[j+1:]
    return new_tour

def tabu_search(distance_matrix, city, algorithm_func, max_iterations=50):
    """
    Busqueda tabú para resolver el problema del agente viajero.

    Parámetros:
    -----------

    distance_matrix ([[int/float]]): Matriz de distancias entre los nodos del
    problema (distance_matrix[i][j] representa la distancia del nodo i al nodo j).
    city (list): Lista de nombres o identificadores de las ciudades o nodos.
    algorithm_func (function): Función de heurística que genera una ruta inicial
    (por ejemplo, nearest_neighbour).
    max_iterations (int, opcional): Número máximo de iteraciones para detener
    el algoritmo. Por defecto es 1000.

    Return:
    ------

    tuple: Una tupla que contiene:
           - best_distance (int/float): La distancia total de la mejor ruta
           encontrada.
           - best_tour (list): La mejor ruta (lista de nodos) encontrada.
    """

    n = len(distance_matrix)

    # Calcula el tamaño de la lista tabú
    tabu_tenure = int(math.sqrt(n))

    # Inicializa la lista tabú
    tabu_list = deque(maxlen=tabu_tenure)
    
    # Calcula la solución inicial x y su distancia
    best_distance, best_tour = algorithm_func(distance_matrix, city)
    
    # Inicializa la solución actual y su distancia
    current_tour = best_tour
    current_distance = best_distance

    patience = 50                 # paciencia
    improvement_threshold = 0.01 # umbral de mejora
    no_improvement_iters = 0     # iteraciones sin mejora
    iteration = 0                # iteraciones

    while iteration < max_iterations:
        neighborhood = []
        
        for i in range(1, n-1):
            for j in range(i+1, n):
                if (i, j) not in tabu_list and (j, i) not in tabu_list:
                    new_tour = two_opt_swap(current_tour, i, j)
                    new_distance = calculate_total_distance(new_tour, distance_matrix)
                    neighborhood.append((new_tour, new_distance, (i, j)))

        # Ordena los movimientos en el vecindario por distancia
        neighborhood.sort(key=lambda x: x[1])

        # Obtiene el mejor movimiento en el vecindario
        best_candidate = neighborhood[0]
        
        new_tour, new_distance, move = best_candidate

        # Verifica el criterio de aspiración
        if move not in tabu_list or new_distance < best_distance:
            current_tour = new_tour
            current_distance = new_distance

            # Verifica si el movimiento es mejor que la mejor solución global
            if new_distance < best_distance:
                best_tour = new_tour
                best_distance = new_distance
            else:
                no_improvement_iters += 1

            tabu_list.append(move)
        else:
            no_improvement_iters += 1
        iteration += 1
        
        # Verifica si se ha alcanzado el número máximo de iteraciones sin mejora
        if no_improvement_iters >= patience and (best_distance - current_distance) / best_distance < improvement_threshold:
            break

    return best_distance, best_tour
