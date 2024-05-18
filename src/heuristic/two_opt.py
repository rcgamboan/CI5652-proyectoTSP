from utils.graficar import graficar_ciudades, graficar_recorrido
from heuristic.nearest_neighbour import nearest_neighbour

def two_opt_local_search(distance_matrix, city, algorithm_func):

    n = len(distance_matrix)
    
    distance, tour = algorithm_func(distance_matrix, city)

    improved = True
    while improved:

        improved = False
        for i in range(n):
            for j in range(i+1, n):
                # Obtener los dos bordes actuales de la ruta
                cur1 = (tour[i], tour[(i+1) % n])
                cur2 = (tour[j], tour[(j+1) % n])
                cur_length = distance_matrix[tour[i]][tour[(i+1) % n]] + distance_matrix[tour[j]][tour[(j+1) % n]]

                # Obtener los dos 'nuevos' bordes para la ruta
                new1 = (tour[i], tour[j])
                new2 = (tour[(i+1) % n], tour[(j+1) % n])
                new_length = distance_matrix[tour[i]][tour[j]] + distance_matrix[tour[(i+1) % n]][tour[(j+1) % n]]

                # Actualizar la ruta, si se mejora
                if new_length < cur_length:
                    # print(f"Intercambiando bordes {cur1} y {cur2} por {new1} y {new2}")
                    tour[i+1:j+1] = tour[i+1:j+1][::-1]
                    improved = True

                    # Dibujar la nueva ruta
                    # graficar_recorrido(tour, city, f"NN iter", True)
                    
    # Calcular la distancia total de la ruta
    distancia_total = sum(distance_matrix[tour[i]][tour[i+1]] for i in range(n))

    return distancia_total, tour