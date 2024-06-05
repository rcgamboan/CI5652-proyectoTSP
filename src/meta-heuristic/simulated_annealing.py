import random
import numpy as np

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
from utils.calcular_distancia import calcular_distancia, calculate_total_distance
from utils.leer_archivo import obtener_ciudades
from utils.graficar import plot_path

from heuristic.random import random_tour
from heuristic.greedy import greedy_insertion
from heuristic.nearest_neighbour import nearest_neighbour
from heuristic.two_opt import two_opt_local_search
from heuristic.double_bridge import iterative_local_search


def simulated_annealing(distance_matrix, initial_solution, initial_temperature, cooling_rate, max_iterations):

    """
    Implementacion de la meta heuristica Simulated Annealing para resolver el problema del TSP
    Simula el proceso de enfriamiento de un material para encontrar la solucion optima
    del problema del TSP
    
    Parámetros:
    ----------
    distance_matrix (lista de listas de floats): Matriz de distancias entre ciudades.
    initial_solution (lista de ints): Solucion inicial al problema del TSP, generada con alguna heuristica.
    initial_temperature (float): Temperatura inicial del sistema.
    cooling_rate (float): Tasa de enfriamiento del sistema.
    max_iterations (int): Numero maximo de iteraciones.

    Returns:
    ------
    best_solution (lista de ints): Mejor ruta encontrada por el algoritmo.
    best_distance (float): Distancia total de la mejor solucion encontrada.

    """
    
    # Se calcula la distancia de la solucion inicial
    current_solution = initial_solution
    best_solution = current_solution
    current_distance = calculate_total_distance(current_solution, distance_matrix)
    best_distance = current_distance
    temperature = initial_temperature

    # Se ejecuta el algoritmo de simulated annealing
    # en cada iteracion se genera una nueva solucion y se evalua si es aceptada
    # si la nueva solucion es mejor que la actual, se actualiza la solucion actual
    # si la nueva solucion es peor que la actual, se acepta con una probabilidad
    # que depende de la temperatura y de la diferencia de distancia entre la solucion actual y la nueva solucion
    for _ in range(max_iterations):

        # Se genera una nueva solucion intercambiando dos ciudades aleatorias
        # se hace swap de dos ciudades aleatorias
        new_solution = current_solution.copy()
        i, j = random.sample(range(len(new_solution)), 2)
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
        
        # Se calcula la distancia de la nueva solucion
        new_distance = calculate_total_distance(new_solution, distance_matrix)

        # Se evalua si la nueva solucion es aceptada
        # si la nueva solucion es mejor que la actual, se actualiza la solucion actual
        if new_distance < current_distance or random.random() < np.exp((current_distance - new_distance) / temperature):
            current_solution = new_solution
            current_distance = new_distance

            if current_distance < best_distance:
                best_solution = current_solution
                best_distance = current_distance

        # Se disminuye la temperatura reduciendo la probabilidad 
        # de aceptar soluciones sub-optimas
        temperature *= cooling_rate

    return best_solution, best_distance

def run_sa(algorithm, distance_matrix, cities_names, initial_temperature, cooling_rate, max_iterations):

    if algorithm == "random":
        _, initial_solution = random_tour(distance_matrix, cities_names, False)
    elif algorithm == "greedy":
        _, initial_solution = greedy_insertion(distance_matrix, cities_names)
    elif algorithm == "nearest_neighbour":
        _, initial_solution = nearest_neighbour(distance_matrix, cities_names)
    elif algorithm == "two_opt_nn":
        _, initial_solution = nearest_neighbour(distance_matrix, cities_names)
        _, initial_solution = two_opt_local_search(distance_matrix, initial_solution,nearest_neighbour)
    elif algorithm == "two_opt_greedy":
        _, initial_solution = greedy_insertion(distance_matrix, cities_names)
        _, initial_solution = two_opt_local_search(distance_matrix, initial_solution,greedy_insertion)
    elif algorithm == "double_bridge_nn":
        _, initial_solution = nearest_neighbour(distance_matrix, cities_names)
        _, initial_solution = iterative_local_search(distance_matrix, initial_solution,nearest_neighbour,False,0)
    elif algorithm == "double_bridge_greedy":
        _, initial_solution = greedy_insertion(distance_matrix, cities_names)
        _, initial_solution = iterative_local_search(distance_matrix, initial_solution,greedy_insertion,False,0)
    elif algorithm == "double_bridge_random":
        _, initial_solution = random_tour(distance_matrix, cities_names, False)
        _, initial_solution = iterative_local_search(distance_matrix, initial_solution,random_tour, False,0)
    else:
        raise ValueError("Algoritmo no válido")

    best_solution, best_distance = simulated_annealing(distance_matrix, 
                                                       initial_solution, 
                                                       initial_temperature, 
                                                       cooling_rate, 
                                                       max_iterations)
    return best_solution, best_distance

cities_names = [
    "berlin52",
    "ch130",
    "tsp225",
    "pcb442",
    "pr1002",
    "pr2392",
    "eg7146",
    "gr9882",
    "it16862",
    "vm22775",
    "rbz43748",
    "sra104815"]

algorithms = ["random", 
              "greedy",  
              "nearest_neighbour",
              "two_opt_nn",
              "two_opt_greedy",
              "double_bridge_nn",
              "double_bridge_greedy",
              "double_bridge_random"]

for i in range(5):
    
    print(f"\nProcesando {cities_names[i]}")
    cities_coords = obtener_ciudades(f"../../doc/Benchmarks/{cities_names[i]}.tsp")
    distance_matrix = np.array(calcular_distancia(cities_coords))

    with open(f"./solutions/{cities_names[i]}_SA.txt", "w") as text_file:
        text_file.write(f"Running SA with {cities_names[i]} data \n\n")

    #initial_temperature = [100, 1000, 5000]
    initial_temperature = [100]
    #cooling_rate = [0.8, 0.9, 0.99]
    cooling_rate = [0.99]
    max_iterations = 10000
    
    for algorithm in algorithms:
        for k in range(len(initial_temperature)):
            for l in range(len(cooling_rate)):
                print(f"Running SA with {algorithm} algorithm")

                best_solution, best_distance = run_sa(algorithm, 
                                                      distance_matrix, 
                                                      cities_coords, 
                                                      initial_temperature[k], 
                                                      cooling_rate[l], 
                                                      max_iterations)

                with open(f"./solutions/{cities_names[i]}_SA.txt", "a") as text_file:
                    text_file.write(f"Algorithm: {algorithm} \n")
                    text_file.write(f"Initial temperature: {initial_temperature[k]} \n")
                    text_file.write(f"Cooling rate: {cooling_rate[l]} \n")
                    text_file.write(f"Max iterations: {max_iterations} \n")
                    text_file.write(f"Mejor distancia: {best_distance} \n")  
                    text_file.write("---------------------------------------------\n\n")

                plot_path(cities_coords, best_solution, best_distance, f"SA_{cities_names[i]}_{algorithm}")
