import random
import numpy as np
from iteration_utilities import random_permutation

import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.calcular_distancia import calcular_distancia, calculate_total_distance
from utils.leer_archivo import obtener_ciudades
from utils.graficar import plot_path


# Se obtiene la población inicial de manera aleatoria
def initial_population(cities_names, population_size):
    """
    Genera una población inicial de individuos.
    
    Parámetros:
    ----------

    cities_list (lista de ints): Lista de ciudades a ser visitadas.
    population_size (int): Tamaño de la población a ser generada.

    Returns:
    ------

    population (lista de listas de ints): Población inicial de individuos.
    """

    population = []
    for _ in range(population_size):
        population.append(random.sample(cities_names, len(cities_names)))
    return population


def aptitude_probability(distance_matrix, population):
    """
    Calcula la probabilidad de aptitud de cada individuo en la población.

    Parámetros:
    ----------

    distance_matrix (lista de listas de floats): Matriz de distancias entre ciudades.
    population (lista de listas de ints): Población de individuos a ser evaluados.

    Returns:
    ------

    population_apt_probs (lista de floats): Probabilidad de aptitud de cada individuo en la población.
    """

    total_distances = [calculate_total_distance(ind, distance_matrix) for ind in population]
    # max_dist = max(population_dist)
    fitness = 1 / np.array(total_distances)
    probabilities = fitness / fitness.sum()
    #population_aptitudes = max_dist - np.array(population_dist)
    #population_apt_probs = population_aptitudes / sum(population_aptitudes)
    return probabilities


def roulette_selection(population, probabilities):
    """
    Selecciona un individuo de la población utilizando el método de la ruleta.

    Parámetros:
    ----------

    population (lista de listas de ints): Población de individuos a ser seleccionados.
    aptitude_probabilities (lista de floats): Probabilidad de aptitud de cada individuo en la población.

    Returns:
    ------

    selected_individual (lista de ints): Individuo seleccionado.
    """

    cumulative_prob = np.cumsum(probabilities)
    r = random.random()
    for i, individual in enumerate(population):
        if r <= cumulative_prob[i]:
            return individual
    #selected_individual_index = np.searchsorted(cumulative_sum_probs, random_value)
    #return population[selected_individual_index]


def triple_crossover(numCities, parents):
    """
    Operador de cruce basado en la combinación de tres padres.

    Parámetros:
    ----------

    numCities (int): Número de ciudades en el problema.
    parents (lista de listas de ints): Tres padres a ser combinados.
    
    Returns:
    ------

    offspring (lista de ints): Descendiente generado por el operador de cruce.
    """

    # Inicializa descendientes
    offspring = [-1] * numCities
    parent1, parent2, parent3 = parents

    # Elije un punto de cruce aleatorio
    crossover_point1 = random.randint(0, numCities - 1)
    crossover_point2 = random.randint(crossover_point1, numCities - 1)

    # Copia el segmento del primer padre al descendiente
    offspring[crossover_point1 : crossover_point2 + 1] = parent1[
        crossover_point1 : crossover_point2 + 1
    ]

    # Rellena el resto de los genes del descendiente usando el segundo y tercer padre
    current_index = (crossover_point2 + 1) % numCities
    for parent in [parent2, parent3]:
        for city in parent:
            if city not in offspring:
                offspring[current_index] = city
                current_index = (current_index + 1) % numCities

    # Si aún hay ciudades sin asignar, completa con las ciudades restantes del primer padre
    for city in parent1:
        if city not in offspring:
            offspring[current_index] = city
            current_index = (current_index + 1) % numCities

    ## Selecciona tres puntos de cruce aleatorios
    #c1, c2, c3 = sorted(random.sample(range(numCities), 3))

    ## Llena los segmentos del descendiente desde cada padre
    #offspring[c1:c2] = parents[0][c1:c2]

    ## Lista de genes ya presentes en el descendiente
    #used_genes = set(offspring[c1:c2])

    ## Completa el segmento siguiente con el segundo padre
    #for gene in parents[1]:
    #    if len(set(offspring)) == numCities:
    #        break
    #    if gene not in used_genes:
    #        for i in range(c2, c3):
    #            if offspring[i] == -1:
    #                offspring[i] = gene
    #                used_genes.add(gene)
    #                break

    ## Rellena los genes restantes con el tercer padre
    #for gene in parents[2]:
    #    if len(set(offspring)) == numCities:
    #        break
    #    if gene not in used_genes:
    #        for i in range(numCities):
    #            if offspring[i] == -1:
    #                offspring[i] = gene
    #                used_genes.add(gene)
    #                break

    # Encontrar el valor faltante
    for i in range(numCities):
        if i not in offspring:
            print(f"Missing value: {i}")
            break

    # Encontrar el valor repetido
    for i in range(numCities):
        if offspring.count(i) > 1:
            print(f"Repeated value: {i}")
            break
    return offspring


def swap_mutation(individual):
    c1, c2 = sorted(random.sample(range(len(individual)), 2))
    individual[c1], individual[c2] = individual[c2], individual[c1]
    return individual


def inversion_mutation(individual):
    """
    Operador de mutación basado en la inversión de segmentos.

    Parámetros:
    ----------

    individual (lista de ints): Individuo a ser mutado.

    Returns:
    ------

    mutated_individual (lista de ints): Individuo mutado.
    """

    c1, c2 = sorted(random.sample(range(len(individual)), 2))
    individual[c1:c2] = reversed(individual[c1:c2])
    return individual


def edge_recombination_mutation(individual):
    """
    Operador de mutación basado en el intercambio de bordes no secuenciales.

    Parámetros:
    ----------
    individual (lista de ints): Individuo a ser mutado.

    Returns:
    ------
    mutated_individual (lista de ints): Individuo mutado.
    """
    # Selecciona dos bordes no secuenciales al azar
    size = len(individual)
    idx1, idx2 = sorted(random.sample(range(size), 2))
    idx1_next = (idx1 + 1) % size
    idx2_next = (idx2 + 1) % size

    # Intercambia los bordes
    individual[idx1_next], individual[idx2_next] = (
        individual[idx2_next],
        individual[idx1_next],
    )
    
    if not is_valid_individual(individual, size):
        print("Invalid individual found in edge_recombination_mutation")
        print(len(individual))
        print(individual)
        raise ValueError("Invalid individual found")

    return individual


#import tsplib95
#from tsp_solver.lkh import solve_tsplib95
#
#
#def lin_kernighan_search(distance_matrix, individual):
#    """
#    Aplicar búsqueda local de Lin-Kernighan (LK) a un individuo.
#
#    Parámetros:
#    ----------
#    distance_matrix (lista de listas de floats): Matriz de distancias entre ciudades.
#    individual (lista de ints): Individuo a ser mejorado.
#
#    Returns:
#    ------
#    improved_individual (lista de ints): Individuo mejorado después de aplicar LK.
#    """
#    # Convertir el recorrido en formato TSPLIB
#    problem = tsplib95.models.StandardProblem()
#    problem.dimension = len(individual)
#    problem.edge_weights = distance_matrix
#
#    # Crear el recorrido en formato TSPLIB
#    tour = [individual[i] + 1 for i in range(len(individual))]
#    tour.append(tour[0])
#
#    # Aplicar la búsqueda local de Lin-Kernighan
#    improved_tour = solve_tsplib95(problem, initial_tour=tour)
#
#    # Convertir el resultado de vuelta al formato original
#    improved_individual = [city - 1 for city in improved_tour[:-1]]
#
#    return improved_individual


def local_search_2opt(individual, distance_matrix):
    """
    Aplica la búsqueda local 2-opt a un individuo.

    Parámetros:
    ----------

    individual (lista de ints): Individuo a ser mejorado.
    distance_matrix (lista de listas de floats): Matriz de distancias entre ciudades.

    Returns:
    ------

    improved_individual (lista de ints): Individuo mejorado después de aplicar 2-opt.
    """

    def two_opt_swap(route, i, k):
        return route[:i] + route[i:k][::-1] + route[k:]

    best = individual
    improved = True
    while improved:
        improved = False
        for i in range(1, len(best) - 2):
            for k in range(i + 1, len(best)):
                new_route = two_opt_swap(best, i, k)
                if calculate_total_distance(
                    new_route, distance_matrix
                ) < calculate_total_distance(best, distance_matrix):
                    best = new_route
                    improved = True
    return best

def is_valid_individual(individual, num_cities):
    return len(individual) == num_cities and len(set(individual)) == num_cities
    #return set(individual) == set(range(num_cities))

def run_memetic_ga(
    cities_coords,
    distance_matrix,
    population_size,
    numGenerations,
    crossover_rate,
    mutation_rate,
    save_every_10_gen=False,
    crossover_method="triple",
    mutation_method="edge_recombination",
    instance_name="",
):
    cities_names = [i for i in range(len(distance_matrix))]
    population = initial_population(cities_names, population_size)

    for generation in range(numGenerations):
        if generation % 10 == 0:
            print("Generation ", generation)

        if generation == 0:
            selected_individuals = population

        random.shuffle(selected_individuals)
        aptitude_probabilities = aptitude_probability(
            distance_matrix, selected_individuals
        )

        # Selecciona los padres
        parents_list = [
            roulette_selection(selected_individuals, aptitude_probabilities)
            for _ in range(int(crossover_rate * population_size))
        ]
        
        # Asegura que el número de padres sea múltiplo de 3
        evolved_offspring = []
        if len(parents_list) % 3 != 0:
            parents_list = parents_list[: -(len(parents_list) % 3)]

        for i in range(0, len(parents_list), 3):
            # Recombina los padres para generar descendientes
            if crossover_method == "triple":
                offspring = triple_crossover(len(cities_names), parents_list[i : i + 3])
            else:
                raise ValueError("Crossover method not valid")

            # Aplica mutación a los descendientes
            if random.random() < mutation_rate:
                if mutation_method == "inversion":
                    offspring = inversion_mutation(offspring)
                elif mutation_method == "swap":
                    offspring = swap_mutation(offspring)
                elif mutation_method == "edge_recombination":
                    offspring = edge_recombination_mutation(offspring)
                else:
                    raise ValueError("Mutation method not valid")
            
            # Aplica búsqueda local 2-opt a los descendientes
            offspring = local_search_2opt(offspring, distance_matrix)
            evolved_offspring.append(offspring)

        evolved_offspring += parents_list

        # Selecciona los mejores individuos de la población actual y la anterior
        # para la siguiente generación
        aptitude_probabilities = aptitude_probability(
            distance_matrix, evolved_offspring
        )
        sorted_indices = np.argsort(aptitude_probabilities)[::-1]
        best_individual_indices = sorted_indices[: int(0.8 * population_size)]
        selected_individuals = [evolved_offspring[i] for i in best_individual_indices]
        previous_population_indices = [
            random.randint(0, population_size - 1)
            for _ in range(int(0.2 * population_size))
        ]
        selected_individuals += [population[i] for i in previous_population_indices]

        #for individual in selected_individuals:
        #    if not is_valid_individual(individual, len(cities_names)):
        #        print("Invalid individual found")
        #        print(f"len(individual) = {len(individual)}")
        #        print(f"len(cities_names) = {len(cities_names)}")
        #        print(individual)
        #        
        #        # Encontrar el valor faltante
        #        for i in range(len(cities_names)):
        #            if i not in individual:
        #                print(f"Missing value: {i}")
        #                break

        #        # Encontrar el valor repetido
        #        for i in range(len(cities_names)):
        #            if individual.count(i) > 1:
        #                print(f"Repeated value: {i}")
        #                break
        #        
        #        raise ValueError("Invalid individual found")

        
        # Guardar la mejor solución cada 100 generaciones
        if save_every_10_gen and (generation % 100 == 0):
            total_dist_all_individuals = [
                calculate_total_distance(ind, distance_matrix)
                for ind in selected_individuals
            ]
            index_minimum = np.argmin(total_dist_all_individuals)
            minimum_distance = min(total_dist_all_individuals)
            shortest_path = selected_individuals[index_minimum]
            shortest_path.append(shortest_path[0])
            plot_path(
                cities_coords,
                shortest_path,
                minimum_distance,
                title=f"MemeticGA_{instance_name}_gen_{generation}",
                folder="memetic-ga",
                display_graph=False,
            )

    return selected_individuals


# Parámetros del algoritmo memético

#population_size = [100, 500, 1000]
population_size = [40, 60, 100]
#crossover_rate = [0.5, 0.7, 0.9]
crossover_rate = [0.9]
#mutation_rate = [0.2, 0.4, 0.6]
mutation_rate = [0.2]
numGenerations = [1500]

crossover_method = "triple"
mutation_method = "edge_recombination"

sol_folder = "memetic-ga"

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
    "sra104815",
]


# Solo las primeras 5 ciudades
for i in range(5):
    cities_coords = obtener_ciudades(f"../../doc/Benchmarks/{cities_names[i]}.tsp")
    with open(
        f"./solutions/{sol_folder}/{cities_names[i]}_{crossover_method}_{mutation_method}.txt", "w"
    ) as text_file:
        text_file.write(f"Running Memetic GA with {cities_names[i]} data \n\n")
    distance_matrix = np.array(calcular_distancia(cities_coords))
    save_every_10_gen = True

    if i == 0:
        population_size = [40]
        numGenerations = [230]
    elif i == 1:
        population_size = [80]
        numGenerations = [450]
    elif i == 2:
        population_size = [120]
        numGenerations = [700]
    elif i == 3:
        population_size = [150]
    else:
        population_size = [400]

    iter = 1
    for j in range(len(population_size)):
        for k in range(len(crossover_rate)):
            for l in range(len(mutation_rate)):
                for m in range(len(numGenerations)):
                    print(
                        f"\nRunning Memetic GA for {cities_names[i]} (iter {iter}/{len(population_size) * len(crossover_rate) * len(mutation_rate) * len(numGenerations)})"
                    )
                    print(f"Num generations: {numGenerations[m]}")
                    print(f"Population size: {population_size[j]}")
                    print(f"Crossover rate: {crossover_rate[k]}")
                    print(f"Mutation rate: {mutation_rate[l]}")

                    ga_solution = run_memetic_ga(
                        cities_coords,
                        distance_matrix,
                        population_size[j],
                        numGenerations[m],
                        crossover_rate[k],
                        mutation_rate[l],
                        save_every_10_gen,
                        crossover_method,
                        mutation_method,
                        instance_name=cities_names[i],
                    )

                    population_dist = [
                        calculate_total_distance(ind, distance_matrix)
                        for ind in ga_solution
                    ]
                    index_minimum = np.argmin(population_dist)
                    shortest_path = ga_solution[index_minimum]
                    minimum_distance = min(population_dist)

                    with open(
                        f"./solutions/{sol_folder}/{cities_names[i]}_{crossover_method}_{mutation_method}.txt",
                        "a",
                    ) as text_file:
                        text_file.write(f"num_generations = {numGenerations[m]}\n")
                        text_file.write(f"population_size = {population_size[j]}\n")
                        text_file.write(f"crossover_rate = {crossover_rate[k]}\n")
                        text_file.write(f"mutation_rate = {mutation_rate[l]}\n")
                        text_file.write(f"minimum_distance = {minimum_distance}\n")
                        text_file.write(f"avg_distance = {np.mean(population_dist)}\n")
                        text_file.write(
                            "---------------------------------------------\n\n"
                        )
                    print(
                        f"saved solution data in ./solutions/{sol_folder}/{cities_names[i]}_{crossover_method}_{mutation_method}.txt"
                    )

                    show_best_route = False
                    shortest_path.append(shortest_path[0])
                    iter += 1
