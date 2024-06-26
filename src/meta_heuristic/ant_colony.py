import numpy as np
import random

def ant_colony_optimization(distance_matrix, n_ants, n_iterations, alpha, beta, rho, Q):
    """
    Implementación del algoritmo de Optimización de Colonia de Hormigas para el TSP.
    
    Parámetros:
    - distance_matrix: matriz de distancias entre ciudades
    - n_ants: número de hormigas
    - n_iterations: número de iteraciones
    - alpha: importancia de las feromonas
    - beta: importancia de la información heurística
    - rho: tasa de evaporación de feromonas
    - Q: constante para la actualización de feromonas
    
    Retorna:
    - best_path: mejor camino encontrado
    - best_cost: costo del mejor camino
    """
    n_cities = len(distance_matrix)
    pheromone = np.ones((n_cities, n_cities))
    best_path = None
    best_cost = float('inf')

    for iteration in range(n_iterations):
        paths = []
        costs = []

        for ant in range(n_ants):
            path = construct_solution(distance_matrix, pheromone, alpha, beta)
            cost = calculate_path_cost(distance_matrix, path)
            paths.append(path)
            costs.append(cost)

            if cost < best_cost:
                best_cost = cost
                best_path = path

        pheromone = update_pheromone(pheromone, paths, costs, rho, Q)
    return best_cost, best_path

def construct_solution(distance_matrix, pheromone, alpha, beta):
    n_cities = len(distance_matrix)
    unvisited = list(range(1, n_cities))
    path = [0]

    while unvisited:
        probabilities = calculate_probabilities(path[-1], unvisited, distance_matrix, pheromone, alpha, beta)
        next_city = random.choices(unvisited, weights=probabilities)[0]
        path.append(next_city)
        unvisited.remove(next_city)

    path.append(0)
    return path

def calculate_probabilities(current_city, unvisited, distance_matrix, pheromone, alpha, beta):
    probabilities = []

    for city in unvisited:
        tau = pheromone[current_city][city]
        eta = 1 / distance_matrix[current_city][city]
        probabilities.append((tau**alpha) * (eta ** beta))
    total = sum(probabilities)
    return [p/total for p in probabilities]

def calculate_path_cost(distance_matrix, path):
    return sum(distance_matrix[path[i]][path[i+1]] for i in range(len(path)-1))

def update_pheromone(pheromone, paths, costs, rho, Q):
    n_cities = len(pheromone)
    pheromone *= (1 - rho)

    for path, cost in zip(paths, costs):
        for i in range(len(path) - 1):
            pheromone[path[i]][path[i+1]] += Q / cost
    
    return pheromone

# Ejemplo de uso
# distance_matrix = ... # Tu matriz de distancias
# best_path, best_cost = ant_colony_optimization(distance_matrix, n_ants=10, n_iterations=100, alpha=1, beta=2, rho=0.5, Q=100)
# print(f"Mejor camino: {best_path}")
# print(f"Mejor costo: {best_cost}")