import random
import numpy as np
from iteration_utilities import random_permutation
import random

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
from utils.calcular_distancia import calcular_distancia, calculate_total_distance
from utils.leer_archivo import obtener_ciudades
from utils.graficar import plot_path

# Se obtiene la poblacion inicial de manera aleatoria
# Los individuos son permutaciones de las ciudades
def initial_population(cities_list, population_size):
    
    """
    Método para obtener la población inicial a ser usada en el algoritmo genético.
    
    Genera populationSize individuos aleatoriamente.
    
    Parámetros:
    ----------
    cities_list (lista de ints): Lista de ciudades a ser permutadas.
    population_size (int): Cantidad de individuos a generar.
    
    Returns:
    ------
    population (Lista de listas de ints): Lista de un individuos.
                                          Cada individuo es una permutación de las ciudades.
    
    Complejidad de tiempo:
    O(n) donde n es la cantidad de individuos a generar.
    """

    population = []
    # Se generan population_size permutaciones aleatorias de las ciudades
    # Es posible que se generen duplicados, pero no se revisan
    # por la baja posibilidad de que ocurra
    for _ in range(population_size):
        population.append(list(random_permutation(cities_list)))
        
    return population

# Funcion para calcular la probabilidad de seleccion de un individuo
# Calcula la aptitud de cada individuo en la población y en base a esta se calcula la probabilidad
# Los individuos con mayor aptitud tienen una mayor probabilidad
# de ser seleccionados como padres para producir descendientes en la siguiente generación
def aptitude_probability(distance_matrix,population):
    
    """
    Método para obtener la probabilidad de aptitud de una población.

    Calcula la probabilidad de aptitud para cada individuo en la población, 
    basándose en la distancia total recorrida por cada individuo.

    Parámetros:
    ----------
    distance_matrix (lista de listas de enteros): Matriz de distancias entre ciudades. 
                                       Cada entrada (i, j) representa la distancia 
                                       entre la ciudad i y la ciudad j.
    population (lista de listas de enteros): Población de individuos. Cada individuo es una permutación 
                                  de las ciudades 

    Returns:
    ------
    population_apt_probs (lista de floats): Lista de probabilidades de aptitud normalizadas 
                                                para cada individuo en la población.

    Complejidad de tiempo:
    O(n), donde n es la cantidad de individuos en la población.
    """
    # Se calcula la aptitud de cada individuo, como la distancia total recorrida
    population_dist = []
    for i in range (len(population)):
        population_dist.append(calculate_total_distance(population[i],distance_matrix))

    # Se calcula la aptitud relativa de cada individuo y
    # se normaliza para obtener la probabilidad de aptitud  
    max_dist = max(population_dist)
    population_aptitudes = max_dist - population_dist
    population_apt_probs = population_aptitudes / sum(population_aptitudes)
    return population_apt_probs

# Mecanismo de seleccion de la ruleta
# Selecciona un individuo de la poblacion basado en la probabilidad
# obtenida según su aptitud
def roulette_selection(population, aptitude_probabilities):

    """
    Operador de seleccion de población utilizando 
    la técnica de la "ruleta" (roulette wheel).

    En este metodo de seleccion se genera un valor aleatorio,
    luego de calcula la suma acumuativa de las probabilidades 
    de aptitud de los individuos en la población, y el primer valor 
    que supere el generado aleatoriamente es seleccionado.

    Parámetros:
    ----------
    population (lista de listas de ints): Población de individuos.
    aptitude_probabilities (lista de floats): Lista de probabilidades de aptitud.

    Returns:
    ------
    selected_individual (lista de ints): Individuo seleccionado según el método de la ruleta

    Complejidad de tiempo:
    O(n), donde n es la cantidad de individuos en la población.
    """

    # Calcula la suma acumulativa de las probabilidades de aptitud
    cumulative_sum_probs = aptitude_probabilities.cumsum()

    # Valor aleatorio entre 0 y 1 para seleccionar un individuo
    random_value = random.random()

    # Encuentra el índice del primer valor acumulativo mayor que el valor aleatorio
    selected_individual_index = len(cumulative_sum_probs[cumulative_sum_probs < random_value]) - 1

    # Retorna el individuo seleccionado
    return population[selected_individual_index]

def crossover(numCities, parents):

    """
    Operador de cruce para combinar dos padres.

    Se utiliza la recombinacion de corte y llenado.
    El cruce combina los genotipos de dos padres para crear descendientes. 
    Se utiliza un punto de corte aleatorio para dividir los padres y generar dos descendientes.
    Se agrega a cada individuo los elementos faltantes del otro padre para completar la permutación.

    Parámetros:
    ----------
    numCities (int): Cantidad total de ciudades/individuos en el problema.
    parents (lista de lista de ints): Padres que seran cruzados.

    Returns:
    ------
    offsprings (lista de listas de enteros): Descendientes generados después del cruce.

    Complejidad de tiempo:
    O(n), donde n es la cantidad de ciudades en el problema.
    """
    # Calcula el punto de corte aleatorio
    cut_index = round(random.uniform(1, len(numCities) - 1))

    # Lista que almacena los descendientes, se trabajará con dos descendientes inicialmente
    # La primera lista almacena el primer descendiente y la segunda lista almacena el segundo descendiente
    offsprings = [[],[]]
    
    # Rellena los descendientes con los elementos de los padres desde el primero hasta el corte
    # En el caso del primero descendiente, se comienza llenando con los elementos del primer padre
    # y se termina con los elementos del segundo padre
    offsprings[0] = parents[0][0:cut_index]
    for city in parents[1]:
        if city not in offsprings[0]:
            offsprings[0].append(city)
    
    # Rellena el segundo descendiente con los elementos del segundo padre hasta el corte
    # y lo termina con los elementos del primer padre
    offsprings[1] = parents[1][0:cut_index]
    for city in parents[0]:
        if city not in offsprings[1]:
            offsprings[1].append(city)

    return offsprings

def run_ga(cities_coords, distance_matrix, population_size, numGenerations,crossover_rate, mutation_rate, save_every_10_gen=False):
    
    """
    Método para ejecutar el algoritmo genético (GA)

    El algoritmo genético evoluciona una población de soluciones 
    candidatas (individuos) para encontrar una solución óptima al TSP.

    Parámetros:
    ----------
    cities_coords (lista de tuplas): Coordenadas (x, y) de las ciudades.
    distance_matrix (lista de listas): Matriz de distancias entre ciudades.
    population_size (int): Tamaño de la población.
    numGenerations (int): Cantidad de generaciones a evolucionar.
    crossover_rate (float): Proporción de individuos seleccionados para el cruce.
    mutation_rate (float): Probabilidad de aplicar la mutación a un individuo.
    save_every_10_gen (bool): Si se deben guardar en un grafico los resultados cada 10 generaciones.

    Returns:
    ------
    selected_individuals (lista de listas): Genotipos de los individuos seleccionados
                                            después de la evolución.

    Complejidad de tiempo:
    O(numGenerations * population_size * numCities), donde numCities es la cantidad de ciudades en el problema.
    """
    # Obtiene los "nombres" de las ciudades
    cities_names = [i for i in range(len(distance_matrix))]

    population = initial_population(cities_names, population_size)

    for generation in range(0, numGenerations+1):
        
        if (generation%10 == 0):
            print("Generation: ", generation)
        
        if generation == 0:
            selected_individuals = population
        
        random.shuffle(selected_individuals)
        
        # Proceso de seleccion
        # Se calcula la probabilidad de seleccionar cada individuo a partir de su aptitud
        aptitude_probabilities = aptitude_probability(distance_matrix,selected_individuals)
        parents_list = []
        # Se seleccionan los padres para el cruce
        # La cantidad de padres seleccionados es proporcional a crossover_rate
        for _ in range(0, int(crossover_rate * population_size)):
            parents_list.append(roulette_selection(selected_individuals,aptitude_probabilities))

        # Proceso de cruce y mutacion
        # Se seleccionan los padres de dos en dos y se cruzan para generar dos hijos por pareja
        evolved_offspring = []    
        for i in range(0,len(parents_list), 2):
            # Se llama a la funcion de cruce con los dos padres
            offsprings = crossover(cities_names,parents_list[i:i+2])

            # Se determina si se aplica mutacion a los hijos
            if(random.random() < mutation_rate):

                # Si ocurre una mutacion, se intercambian dos ciudades aleatorias en cada hijo
                point1 = random.randint(0, len(cities_names) - 1)
                point2 = random.randint(0, len(cities_names) - 1)
                offsprings[0][point1], offsprings[0][point2] = (offsprings[0][point2],offsprings[0][point1])

                point1 = random.randint(0, len(cities_names) - 1)
                point2 = random.randint(0, len(cities_names) - 1)
                offsprings[1][point1], offsprings[1][point2] = (offsprings[1][point2],offsprings[1][point1])

            evolved_offspring.append(offsprings[0])
            evolved_offspring.append(offsprings[1])

        # Se mezclan los padres y los hijos evolucionados
        evolved_offspring += parents_list
        aptitude_probabilities = aptitude_probability(distance_matrix,evolved_offspring)
        
        # Se seleccionan los individuos con mejor aptitud para la siguiente generacion
        # Se selecciona el 80% de los individuos con mejor aptitud
        sorted_indices = np.argsort(aptitude_probabilities)[::-1]
        best_individual_indices = sorted_indices[0:int(0.8*population_size)]

        selected_individuals = []
        for i in best_individual_indices:
            selected_individuals.append(evolved_offspring[i])
        
        # Se selecciona el 20% restante de los individuos con peor aptitud
        previous_population_indices = [random.randint(0, (population_size - 1)) for _ in range(int(0.2*population_size))]
        for i in previous_population_indices:
            selected_individuals.append(population[i])
        
        if save_every_10_gen:
            if (generation%10 == 0):
                total_dist_all_individuals = []
                for i in range(0, population_size):
                    total_dist_all_individuals.append(calculate_total_distance(selected_individuals[i],distance_matrix))

                index_minimum = np.argmin(total_dist_all_individuals)
                minimum_distance = min(total_dist_all_individuals)

                shortest_path = selected_individuals[index_minimum]
                plot_path(cities_coords, shortest_path, minimum_distance, title=f"Generation {generation}")
            
    return selected_individuals

##### Parametros del algoritmo genetico

# Tamaño de la poblacion
population_size = 300
# Tasa de cruce, es decir, la proporcion de individuos seleccionados de la poblacion
# en cada generacion para el cruce
crossover_rate = 0.7
# Tasa de mutacion, es decir, la probabilidad de que ocurra una mutacion
mutation_rate = 0.2
# Numero de generaciones, es decir, el numero de iteraciones del algoritmo genetico
numGenerations = 200

# Nombres de algunos de los problemas TSP disponibles
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

for i in range(len(cities_names)):
    # Se obtienen las coordenadas de las ciudades
    cities_coords = obtener_ciudades(f"../../doc/Benchmarks/{cities_names[i]}.tsp")

    # Se calcula la matriz de distancias
    distance_matrix = np.array(calcular_distancia(cities_coords))

    # Guardar imagenes de la mejor solucion cada 10 generaciones
    # Las imagenes se guardan actualmente en la carpeta gens del directorio actual
    save_every_10_gen = False
    
    print(f"Running GA for {cities_names[i]}")
    # Se ejecuta el algoritmo genetico con los parametros especificados
    ga_solution = run_ga(cities_coords, 
                        distance_matrix, 
                        population_size,
                        numGenerations, 
                        crossover_rate, 
                        mutation_rate, 
                        save_every_10_gen)

    # Al finalizar el algoritmo genetico, se tiene una poblacion de soluciones
    # Se calcula la distancia total de cada solucion y se selecciona la mejor
    population_dist = []
    for j in range(0, population_size):
        population_dist.append(calculate_total_distance(ga_solution[j],distance_matrix))

    index_minimum = np.argmin(population_dist)
    shortest_path = ga_solution[index_minimum]
    minimum_distance = min(population_dist)

    # Mostrar el grafico de la mejor obtenida por el algoritmo genetico
    show_best_route = False
    plot_path(cities_coords,shortest_path, minimum_distance, f"{cities_names[i]}_best_route",show_best_route)
    print(f"saved {cities_names[i]} best route graph in ../../img/genetic-algorithm/{cities_names[i]}_best_route.png")

    print(f"{cities_names[i]} minimum distance using GA : {minimum_distance}\n")