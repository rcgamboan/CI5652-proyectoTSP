import random
from utils.graficar import graficar_recorrido


def random_tour(distance_matrix, cities, save_iterations = False, current_city = ""):
    """
    Genera una ruta aleatoria para la resolución del problema del agente viajero (TSP).

    Esta función selecciona aleatoriamente un nodo inicial y genera una ruta
    visitando todos los nodos de manera aleatoria. 

    Parámetros:
    ----------

    distance_matrix ([[int/float]]): Matriz de distancias entre los nodos del problema.
                                     (distance_matrix[i][j] representa la
                                     distancia del nodo i al nodo j).
    cities (list): Lista de nombres o identificadores de las ciudades o nodos.

    Return:
    ------

    tuple: Una tupla que contiene:
           - total_distance (int/float): La distancia total de la ruta encontrada.
           - tour (list): La ruta (lista de nodos) encontrada.

    """

    n = len(distance_matrix)
    # Seleccionar un nodo inicial aleatorio
    initial_node = random.randint(0, n - 1)

    tour = [initial_node]

    visited = set(tour)
    non_visited = set([i for i in range(n)])
    non_visited = non_visited - visited

    i = 0
    while len(visited) < n:

        # Seleccionar aleatoriamente el siguiente nodo de la ruta
        next_node = random.choice(list(non_visited))
        tour.append(next_node)
        visited.add(next_node)
        non_visited = non_visited - set([next_node])

        if save_iterations:
            graficar_recorrido(
                tour, 
                cities, 
                f"random/{current_city}" , 
                f"{current_city}_random_tour_iter_{i}", 
                False
            )
            
        i += 1

    # Agregar el nodo inicial al final de la ruta para completar el ciclo
    tour.append(initial_node)

    # Calcular la distancia total de la ruta
    total_distance = sum(distance_matrix[tour[i - 1]][tour[i]] for i in range(n + 1))

    return total_distance, tour
