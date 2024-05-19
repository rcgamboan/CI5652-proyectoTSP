import random


def random_tour(distance_matrix, cities):

    n = len(distance_matrix)
    # Seleccionar un nodo inicial aleatorio
    initial_node = random.randint(0, n - 1)

    tour = [initial_node]

    visited = set(tour)
    non_visited = set([i for i in range(n)])
    non_visited = non_visited - visited

    while len(visited) < n:

        # Seleccionar aleatoriamente el siguiente nodo de la ruta
        next_node = random.choice(list(non_visited))
        tour.append(next_node)
        visited.add(next_node)
        non_visited = non_visited - set([next_node])

    # Agregar el nodo inicial al final de la ruta para completar el ciclo
    tour.append(initial_node)

    # Calcular la distancia total de la ruta
    total_distance = sum(distance_matrix[tour[i - 1]][tour[i]] for i in range(n + 1))

    return total_distance, tour
