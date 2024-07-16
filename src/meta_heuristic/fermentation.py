import numpy as np
import random

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
from utils.calcular_distancia import calcular_distancia, calculate_total_distance
from utils.leer_archivo import obtener_ciudades

# Generar una solución inicial aleatoria
def generate_initial_solution(cities):
    return random.sample(cities, len(cities))

# Evaluación de soluciones basada en energía (calidad de la solución)
def evaluate_solutions(population, distance_matrix):
    return [(solution, calculate_total_distance(solution, distance_matrix)) for solution in population]

# Metabolismo: Consumo de nutrientes y producción de energía
def metabolize_solutions(evaluated_solutions, nutrient_factor):
    total_energy = sum(1 / distance for _, distance in evaluated_solutions)
    return [(solution, (1 / distance) / total_energy * nutrient_factor) for solution, distance in evaluated_solutions]

# Producción de subproductos usando operadores 2-opt
def produce_subproducts(solution):
    subproduct = solution[:]
    a, b = random.sample(range(len(subproduct)), 2)
    if a > b:
        a, b = b, a
    subproduct[a:b] = reversed(subproduct[a:b])
    return subproduct

# Adaptación y mutación
def adapt_and_mutate(solution, mutation_rate):
    if random.random() < mutation_rate:
        a, b = random.sample(range(len(solution)), 2)
        solution[a], solution[b] = solution[b], solution[a]
    return solution

# Mejora local utilizando el operador 2-opt
def local_search(solution, distance_matrix):
    best = solution
    improved = True
    while improved:
        improved = False
        for i in range(1, len(solution) - 1):
            for j in range(i + 1, len(solution)):
                if j - i == 1:
                    continue
                new_solution = solution[:]
                new_solution[i:j] = reversed(solution[i:j])
                if calculate_total_distance(new_solution, distance_matrix) < calculate_total_distance(best, distance_matrix):
                    best = new_solution
                    improved = True
        solution = best
    return best

# Optimización por Fermentación
def fermentation_optimization(cities, 
                              distance_matrix, 
                              iterations, 
                              population_size, 
                              mutation_rate):
    # Inicialización de la población
    population = [generate_initial_solution(cities) for _ in range(population_size)]
    best_solution = min(population, key=lambda s: calculate_total_distance(s, distance_matrix))
    best_distance = calculate_total_distance(best_solution, distance_matrix)
    
    for i in range(iterations):
        # Evaluación inicial
        evaluated_solutions = evaluate_solutions(population, distance_matrix)
        
        # Metabolismo y producción de energía
        nutrient_factor = 1 - (i / iterations)  # Disminución de nutrientes con el tiempo
        metabolized_solutions = metabolize_solutions(evaluated_solutions, nutrient_factor)
        
        # Producción de subproductos
        subproducts = [produce_subproducts(solution) for solution, _ in metabolized_solutions]
        
        # Adaptación y mutación
        new_population = [adapt_and_mutate(subproduct, mutation_rate) for subproduct in subproducts]
        
        # Aplicar mejora local a la nueva población
        new_population = [local_search(solution, distance_matrix) for solution in new_population]
        
        # Evaluación de la nueva población
        evaluated_new_population = evaluate_solutions(new_population, distance_matrix)
        
        # Reemplazo y evolución
        population = [solution for solution, _ in evaluated_new_population]
        current_best = min(population, key=lambda s: calculate_total_distance(s, distance_matrix))
        current_best_distance = calculate_total_distance(current_best, distance_matrix)
        if current_best_distance < best_distance:
            best_solution = current_best
            best_distance = current_best_distance
    
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

for i in range(4):
    cities_coords = obtener_ciudades(f"../../doc/Benchmarks/{cities_names[i]}.tsp")
    distance_matrix = np.array(calcular_distancia(cities_coords))

    best_solution, best_distance = fermentation_optimization(list(range(len(cities_coords))), 
                                                             distance_matrix, 
                                                             iterations=10, 
                                                             population_size=10, 
                                                             mutation_rate=0.1)

    print(f"Mejor solución para {cities_names[i]}: {best_solution}")
    print(f"Mejor distancia para {cities_names[i]}: {best_distance}")