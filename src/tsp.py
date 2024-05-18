# CI5652 - Diseño de Algoritmos II
# Proyecto Traveling Salesman Problem - Corte 1
# Integrantes:
    # Abel Zavaleta, 
    # Alejandro Meneses, 
    # Roberto Gamboa, 16-10394 

import time
from utils.file_names import FILE_NAMES, LABEL_NAMES
from utils.graficar import graficar_ciudades, graficar_recorrido
from utils.display_table import display_table
from utils.calcular_distancia import calcular_distancia, calcular_costo_ruta
from utils.leer_archivo import obtener_ciudades, obtener_mejor_ruta
from heuristic.random import random_tour
from heuristic.greedy import greedy_insertion, greedy_insertion_mejor_inicio
from heuristic.nearest_neighbour import nearest_neighbour, nearest_neighbour_mejor_inicio
from heuristic.two_opt import two_opt_local_search


def run_algorithm(name, save_graph, show_on_screen, algorithm_func, *args):

    cols.append(name)

    start_time = time.time()
    result = algorithm_func(*args)
    end_time = time.time()

    execution_time = round(end_time - start_time, 5)
    distance, tour = result

    print(f"\n{LABEL_NAMES[name]}")
    print(f"Distancia total: {round(distance, 2)}")
    print(f"Tiempo de ejecución: {execution_time} segundos")

    data.append([round(distance, 2), execution_time, ""])

    if save_graph:
        graficar_recorrido(tour, nodes, f"{FILE_NAMES[name]}{currentCity}", show_on_screen)

    return result

if __name__ == "__main__":
    
    # cities = [ "berlin52", "ch130", "tsp225", "pcb442", "pr1002"]
    cities = ["berlin52"]

    for currentCity in cities:

        cols = ["best_tour"]
        data = []
        
        nodes = obtener_ciudades(f"../doc/Benchmarks/{currentCity}.tsp")
        best_tour = obtener_mejor_ruta(f"../doc/Benchmarks/{currentCity}.opt.tour")

        #Calculamos las distacion entre nodos y calculamos el costo de la mejor ruta del bechnmark
        distance_matrix = calcular_distancia(nodes)
        best_distance_tour = calcular_costo_ruta(best_tour, distance_matrix)
        
        print(f"Distancia minima posible para {currentCity}: {best_distance_tour}")
        data.append([round(best_distance_tour,2), 'N/A', ""])

        show_on_screen = False
        
        graficar_ciudades(nodes, currentCity, show_on_screen)
        graficar_recorrido(best_tour, nodes, f"{FILE_NAMES["best_tour"]}{currentCity}", show_on_screen)

        ########################## INITIAL TOUR ##########################
        save_graph = True
        show_on_screen = False
        show_each_iteration = False

        # RANDOM
        distance_random, tour_random = run_algorithm(
            "random_tour", 
            save_graph, 
            show_on_screen,
            random_tour, 
            distance_matrix,
            nodes,
        )

        # NEAREST NEIGHBOUR
        distance_NN, tour_NN = run_algorithm(
            "nn", 
            save_graph, 
            show_on_screen,
            nearest_neighbour, 
            distance_matrix, 
            nodes, 
            0, 
            show_each_iteration,
        )

        # distance_NN_iteration, tour_NN_iteration = run_algorithm(
        #     "nn_ite",
        #     save_graph, 
        #     show_on_screen,
        #     nearest_neighbour_mejor_inicio, 
        #     distance_matrix, 
        #     nodes
        # )

        # GREEDY
        distance_greedy, tour_greedy = run_algorithm(
            "greedy",
            save_graph, 
            show_on_screen,
            greedy_insertion, 
            distance_matrix, 
            nodes, 0, 
            show_each_iteration,
        )

        # distance_greedy_iteration, tour_greedy_iteration = run_algorithm(
        #     "greedy_ite",
        #     save_graph, 
        #     show_on_screen,
        #     greedy_insertion_mejor_inicio, 
        #     distance_matrix, 
        #     nodes
        # )

        display_table(cols, data, currentCity, "table_initial")


        ########################## LOCAL SEARCH ##########################

        cols = ["best_tour"]
        data = []
        data.append([round(best_distance_tour,2), 'N/A', ""])

        save_graph = True
        show_on_screen = False
        show_each_iteration = False

        # RANDOM
        distance_random, tour_random = run_algorithm(
            "two_opt_random", 
            save_graph, 
            show_on_screen,
            two_opt_local_search,
            distance_matrix, 
            nodes,
            random_tour
        )

        # NEAREST NEIGHBOUR
        distance_two_opt_nn, tour_two_opt_nn = run_algorithm(
            "two_opt_nn", 
            save_graph, 
            show_on_screen,
            two_opt_local_search, 
            distance_matrix, 
            nodes,
            nearest_neighbour
        )

        # GREEDY
        distance_two_opt_greedy, tour_two_opt_greedy = run_algorithm(
            "two_opt_greedy", 
            save_graph, 
            show_on_screen,
            two_opt_local_search, 
            distance_matrix, 
            nodes,
            greedy_insertion
        )

        display_table(cols, data, currentCity, "table_local_search")
        