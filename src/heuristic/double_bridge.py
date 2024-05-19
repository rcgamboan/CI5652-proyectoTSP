from random import randrange
from heuristic.two_opt import two_opt_local_search


def calculate_total_distance(tour, distance_matrix):
    """
    Calcula la distancia total de un recorrido.
    """
    total_distance = 0
    for i in range(len(tour)):
        # Agrega la distancia entre la actual ciudad y la siguiente ciudad
        total_distance += distance_matrix[tour[i]][tour[(i + 1) % len(tour)]]
    return total_distance


def double_bridge_move(tour):
    """
    Realiza el movimiento de doble puente en un recorrido determinado.
    """
    n = len(tour)

    pos1 = 1 + randrange(n // 4)
    pos2 = pos1 + 1 + randrange(n // 4)
    pos3 = pos2 + 1 + randrange(n // 4)

    p1 = tour[0:pos1] + tour[pos3:]
    p2 = tour[pos2:pos3] + tour[pos1:pos2]

    return p1 + p2


def iterative_local_search(
    distance_matrix, city, algorithm_func, max_no_improv_iters=50
):
    """
    Búsqueda local iterativa para la resolución del problema del agente viajero (TSP).

    El método mejora iterativamente una solución inicial mediante una
    combinación de movimientos de perturbación (doble puente) y búsqueda local
    (2-opt). El proceso continúa hasta que se alcanza un número máximo
    de iteraciones sin mejora.

    Parámetros:
    ----------

    distance_matrix ([[int/float]]): Matriz de distancias entre los nodos del
                                     problema (distance_matrix[i][j] representa
                                     la distancia del nodo i al nodo j).
    city (list): Lista de nombres o identificadores de las ciudades o nodos.
    algorithm_func (function): Función de heurística que genera una ruta inicial
    (por ejemplo, nearest_neighbour).
    max_no_improv_iters (int, opcional): Número máximo de iteraciones sin
    mejora para detener el algoritmo. Por defecto es 50.

    Return:
    ------

    tuple: Una tupla que contiene:
           - best_distance (int/float): La distancia total de la mejor ruta
           encontrada.
           - best_tour (list): La mejor ruta (lista de nodos) encontrada.
    """

    # Genera una solucion inicial
    best_distance, best_tour = two_opt_local_search(
        distance_matrix, city, algorithm_func
    )
    no_improv_iters = 0

    while no_improv_iters < max_no_improv_iters:
        # Aplica el movimiento de doble puente (perturbacion)
        new_tour = double_bridge_move(best_tour)

        # Aplica la busqueda local sobre la solucion perturbada
        new_distance, new_tour = two_opt_local_search(
            distance_matrix, city, lambda dm, c: (0, new_tour)
        )

        # Criterio de aceptacion
        if new_distance < best_distance:
            best_distance, best_tour = new_distance, new_tour
            no_improv_iters = 0
        else:
            no_improv_iters += 1

    return best_distance, best_tour
