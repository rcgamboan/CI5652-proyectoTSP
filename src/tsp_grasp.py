# CI5652 - Diseño de Algoritmos II
# Proyecto Traveling Salesman Problem - Corte 1
# Integrantes:
# Abel Zavaleta,
# Alejandro Meneses,
# Roberto Gamboa, 16-10394

import time, math
from utils.generate_timelapse import generate_timelapse
from utils.file_names import FILE_NAMES, LABEL_NAMES
from utils.graficar import graficar_ciudades, graficar_recorrido
from utils.display_table import display_table, display_summary_table
from utils.calcular_distancia import calcular_distancia, calcular_costo_ruta
from utils.leer_archivo import obtener_ciudades, obtener_mejor_ruta
from heuristic.random import random_tour
from heuristic.greedy import greedy_insertion, greedy_insertion_mejor_inicio
from heuristic.nearest_neighbour import (
    nearest_neighbour,
    nearest_neighbour_mejor_inicio,
)
from heuristic.two_opt import two_opt_local_search
from heuristic.double_bridge import iterative_local_search
from meta_heuristic.tabu_search import tabu_search
from meta_heuristic.grasp import grasp
from meta_heuristic.ant_colony import ant_colony_optimization


global best_distance_tour

def calcular_cercania(best, current):
    cercania = (1 - abs((current-best)/current)) * 100
    return str("{:.2f}".format(cercania)) + "%"

def run_algorithm(name, current_city, save_graph, show_on_screen, algorithm_func, *args):

    start_time = time.time()
    result = algorithm_func(*args)
    end_time = time.time()

    execution_time = round(end_time - start_time, 5)
    distance, tour = result

    print(f"\n{LABEL_NAMES[name]}")
    print(f"Distancia total: {round(distance, 2)}")
    print(f"Tiempo de ejecución: {execution_time} segundos")

    if save_graph:
        graficar_recorrido(
            tour, nodes, "", f"{FILE_NAMES[name]}{current_city}", show_on_screen
        )
    
    return (distance, tour, "{:.2f}".format(execution_time))

if __name__ == "__main__":

    cities = [ "berlin52", "ch130", "tsp225", "pcb442", "pr1002"]
    # cities = ["berlin52"]
    data = []

    # cols = ["best_tour", "random_tour", "nn", "two_opt_nn", "double_bridge_nn","grasp", "ant_colony"]
    # cols = ["best_tour","grasp","ant_colony"]
    # for currentCity in cities:

    #     row = []

    #     nodes = obtener_ciudades(f"../doc/Benchmarks/{currentCity}.tsp")
    #     best_tour = obtener_mejor_ruta(f"../doc/Benchmarks/{currentCity}.opt.tour")

    #     # Calculamos las distacion entre nodos y calculamos el costo de la mejor ruta del bechnmark
    #     distance_matrix = calcular_distancia(nodes)
    #     best_distance_tour = calcular_costo_ruta(best_tour, distance_matrix)

    #     print(f"Distancia minima posible para {currentCity}: {best_distance_tour}")
        
    #     row.append(calcular_cercania(best_distance_tour, best_distance_tour))
    #     show_on_screen = False

    #     graficar_ciudades(nodes, currentCity, show_on_screen)
    #     graficar_recorrido(
    #         best_tour, nodes, "", f"{FILE_NAMES["best_tour"]}{currentCity}", show_on_screen
    #     )

    #     save_graph = True
    #     show_on_screen = False
    #     show_each_iteration = False

    #     # RANDOM
    #     distance_random, tour_random, t = run_algorithm(
    #         "random_tour",
    #         currentCity,
    #         save_graph,
    #         show_on_screen,
    #         random_tour,
    #         distance_matrix,
    #         nodes,
    #         show_each_iteration
    #     )
    #     row.append(calcular_cercania(best_distance_tour, distance_random))
        
    #     # # NEAREST NEIGHBOUR
    #     distance_NN, tour_NN, t = run_algorithm(
    #         "nn",
    #         currentCity,
    #         save_graph,
    #         show_on_screen,
    #         nearest_neighbour,
    #         distance_matrix,
    #         nodes,
    #         show_each_iteration
    #     )
    #     row.append(calcular_cercania(best_distance_tour, distance_NN))

    #     # ########################## LOCAL SEARCH ##########################
    #     # # NEAREST NEIGHBOUR
    #     distance_two_opt_nn, tour_two_opt_nn, t = run_algorithm(
    #         "two_opt_nn",
    #         currentCity,
    #         save_graph,
    #         show_on_screen,
    #         two_opt_local_search,
    #         distance_matrix,
    #         nodes,
    #         nearest_neighbour,
    #         show_each_iteration
    #     )
    #     row.append(calcular_cercania(best_distance_tour, distance_two_opt_nn))
    #     # ########################## ITERATED LOCAL SEARCH ##########################
    #     # # NEAREST NEIGHBOUR
    #     distance_double_bridge_nn, double_bridge_opt_nn, t = run_algorithm(
    #         "double_bridge_nn",
    #         currentCity,
    #         save_graph,
    #         show_on_screen,
    #         iterative_local_search,
    #         distance_matrix,
    #         nodes,
    #         nearest_neighbour,
    #         show_each_iteration
    #     )
    #     row.append(calcular_cercania(best_distance_tour, distance_double_bridge_nn))

    #     # NEAREST NEIGHBOUR
    #     # print("\nNEAREST NEIGHBOUR")
    #     # start_time = time.time()
    #     # distance_tabu_search_nn, tour_tabu_search_nn = tabu_search(distance_matrix, nodes, nearest_neighbour)
    #     # end_time = time.time()
    #     # print(f"distancia total: {distance_tabu_search_nn}")

    #     # execution_time = round(end_time - start_time, 5)

    #     # row.append(calcular_cercania(best_distance_tour, distance_tabu_search_nn))

    #     # GRASP
    #     distance_grasp, tour_graps, t = run_algorithm(
    #         "grasp",
    #         currentCity,
    #         save_graph,
    #         show_on_screen,
    #         grasp,
    #         distance_matrix,
    #         nodes,
    #         0.5
    #     )

    #     row.append(calcular_cercania(best_distance_tour, distance_grasp))

    #     # ANC
    #     print("\nAnt Colony")
    #     start_time = time.time()
    #     distance_anc, tour_anc = ant_colony_optimization(distance_matrix, n_ants=10, n_iterations=100, alpha=1, beta=2, rho=0.5, Q=100)
    #     end_time = time.time()
    #     print(f"distancia total: {distance_anc}")

    #     execution_time = round(end_time - start_time, 5)
    #     print(f"Tiempo de ejecución: {execution_time} segundos")


    #     row.append(calcular_cercania(best_distance_tour, distance_anc))


    #     data.append(row)
    # display_summary_table(cities, cols, data)

    cols = ["20", "40", "60", "80", "100"]
    for currentCity in cities:

        row = []

        nodes = obtener_ciudades(f"../doc/Benchmarks/{currentCity}.tsp")
        best_tour = obtener_mejor_ruta(f"../doc/Benchmarks/{currentCity}.opt.tour")

        # Calculamos las distacion entre nodos y calculamos el costo de la mejor ruta del bechnmark
        distance_matrix = calcular_distancia(nodes)
        best_distance_tour = calcular_costo_ruta(best_tour, distance_matrix)

        print(f"Distancia minima posible para {currentCity}: {best_distance_tour}")
        
        # row.append(calcular_cercania(best_distance_tour, best_distance_tour))

        # ANC
        print("\nAnt Colony")
        start_time = time.time()
        distance_anc, tour_anc = ant_colony_optimization(distance_matrix, n_ants=20, n_iterations=100, alpha=1, beta=2, rho=0.5, Q=100)
        end_time = time.time()
        print(f"distancia total: {distance_anc}")

        execution_time = round(end_time - start_time, 5)
        print(f"Tiempo de ejecución: {execution_time} segundos")

        row.append(calcular_cercania(best_distance_tour, distance_anc))

        # ANC
        print("\nAnt Colony")
        start_time = time.time()
        distance_anc, tour_anc = ant_colony_optimization(distance_matrix, n_ants=40, n_iterations=100, alpha=1, beta=2, rho=0.5, Q=100)
        end_time = time.time()
        print(f"distancia total: {distance_anc}")

        execution_time = round(end_time - start_time, 5)
        print(f"Tiempo de ejecución: {execution_time} segundos")

        row.append(calcular_cercania(best_distance_tour, distance_anc))

        # ANC
        print("\nAnt Colony")
        start_time = time.time()
        distance_anc, tour_anc = ant_colony_optimization(distance_matrix, n_ants=60, n_iterations=100, alpha=1, beta=2, rho=0.5, Q=100)
        end_time = time.time()
        print(f"distancia total: {distance_anc}")

        execution_time = round(end_time - start_time, 5)
        print(f"Tiempo de ejecución: {execution_time} segundos")

        row.append(calcular_cercania(best_distance_tour, distance_anc))

        # ANC
        print("\nAnt Colony")
        start_time = time.time()
        distance_anc, tour_anc = ant_colony_optimization(distance_matrix, n_ants=80, n_iterations=100, alpha=1, beta=2, rho=0.5, Q=100)
        end_time = time.time()
        print(f"distancia total: {distance_anc}")

        execution_time = round(end_time - start_time, 5)
        print(f"Tiempo de ejecución: {execution_time} segundos")

        row.append(calcular_cercania(best_distance_tour, distance_anc))

        # ANC
        print("\nAnt Colony")
        start_time = time.time()
        distance_anc, tour_anc = ant_colony_optimization(distance_matrix, n_ants=100, n_iterations=100, alpha=1, beta=2, rho=0.5, Q=100)
        end_time = time.time()
        print(f"distancia total: {distance_anc}")

        execution_time = round(end_time - start_time, 5)
        print(f"Tiempo de ejecución: {execution_time} segundos")

        row.append(calcular_cercania(best_distance_tour, distance_anc))


        data.append(row)
    display_summary_table(cities, cols, data)

    # cols = ["best_tour", "alpha_0", "alpha_0.25", "alpha_0.5", "alpha_0.75", "alpha_1"]

    # for currentCity in cities:

    #     row = []

    #     nodes = obtener_ciudades(f"../doc/Benchmarks/{currentCity}.tsp")
    #     best_tour = obtener_mejor_ruta(f"../doc/Benchmarks/{currentCity}.opt.tour")

    #     # Calculamos las distacion entre nodos y calculamos el costo de la mejor ruta del bechnmark
    #     distance_matrix = calcular_distancia(nodes)
    #     best_distance_tour = calcular_costo_ruta(best_tour, distance_matrix)

    #     print(f"Distancia minima posible para {currentCity}: {best_distance_tour}")
        
    #     row.append(calcular_cercania(best_distance_tour, best_distance_tour))
    #     show_on_screen = False

    #     graficar_ciudades(nodes, currentCity, show_on_screen)
    #     graficar_recorrido(
    #         best_tour, nodes, "", f"{FILE_NAMES["best_tour"]}{currentCity}", show_on_screen
    #     )

    #     ########################## INITIAL TOUR ##########################
    #     save_graph = True
    #     show_on_screen = False
    #     show_each_iteration = False

    #     # GRASP
    #     distance_grasp, tour_graps, t = run_algorithm(
    #         "grasp",
    #         currentCity,
    #         save_graph,
    #         show_on_screen,
    #         grasp,
    #         distance_matrix,
    #         nodes,
    #         0
    #     )
    #     row.append(calcular_cercania(best_distance_tour, distance_grasp))

    #     # GRASP
    #     distance_grasp, tour_graps, t = run_algorithm(
    #         "grasp",
    #         currentCity,
    #         save_graph,
    #         show_on_screen,
    #         grasp,
    #         distance_matrix,
    #         nodes,
    #         0.25
    #     )
    #     row.append(calcular_cercania(best_distance_tour, distance_grasp))

    #     distance_grasp, tour_graps, t = run_algorithm(
    #         "grasp",
    #         currentCity,
    #         save_graph,
    #         show_on_screen,
    #         grasp,
    #         distance_matrix,
    #         nodes,
    #         0.5
    #     )
    #     row.append(calcular_cercania(best_distance_tour, distance_grasp))

    #     distance_grasp, tour_graps, t = run_algorithm(
    #         "grasp",
    #         currentCity,
    #         save_graph,
    #         show_on_screen,
    #         grasp,
    #         distance_matrix,
    #         nodes,
    #         0.75
    #     )
    #     row.append(calcular_cercania(best_distance_tour, distance_grasp))

    #     distance_grasp, tour_graps, t = run_algorithm(
    #         "grasp",
    #         currentCity,
    #         save_graph,
    #         show_on_screen,
    #         grasp,
    #         distance_matrix,
    #         nodes,
    #         1
    #     )
    #     row.append(calcular_cercania(best_distance_tour, distance_grasp))
    #     data.append(row)

    # display_summary_table(cities, cols, data)


