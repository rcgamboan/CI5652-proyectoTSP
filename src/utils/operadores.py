import random
import numpy as np

from utils.calcular_distancia import calcular_distancia, calculate_total_distance

def is_valid_individual(individual, num_cities):
    return len(individual) == num_cities and len(set(individual)) == num_cities
    #return set(individual) == set(range(num_cities))


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
