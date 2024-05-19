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
    Realiza una búsqueda local iterativa (ILS) con perturbación de doble puente.

    Parámetros:
    ----------

    Distance_matrix (lista de lista de float): una lista 2D que representa las
    distancias entre cada par de ciudades.
    city (lista de tuplas de float): una lista de coordenadas para cada ciudad.
    algoritmo_func (función): Función que genera un recorrido inicial y su distancia.
    La firma es algorithm_func(distance_matrix, city) -> (distance, tour).

    Returns:
    -------

    tupla: una tupla que contiene:
        - best_distance (float): La distancia total del mejor recorrido encontrado.
        - best_tour (lista de int): La secuencia de índices de ciudades que representan
        el mejor recorrido encontrado.
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
