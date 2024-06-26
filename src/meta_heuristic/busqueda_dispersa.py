import random
import numpy as np
from iteration_utilities import random_permutation

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
from utils.calcular_distancia import calcular_distancia, calculate_total_distance
from utils.leer_archivo import obtener_ciudades
from utils.graficar import plot_path
from utils.operadores import *

def initial_population(cities_list, tam_conjunto):
    """
    Método para obtener el conjunto de referencia inicial.
    
    Genera tam_conjunto puntos de referencia aleatoriamente.
    
    Parámetros:
    ----------
    cities_list (lista de ints): Listo con los "nombres" de las ciudades.
    tam_conjunto (int): Cantidad de puntos de referencia a generar.
    
    Returns:
    ------
    conjunto_referencia (Lista de listas de ints): Conjunto de referencia.
    
    Complejidad de tiempo:
    O(n) donde n es la cantidad de puntos a generar.
    """

    conjunto_referencia = []
    for _ in range(tam_conjunto):
        conjunto_referencia.append(list(random_permutation(cities_list)))
        
    return conjunto_referencia

def distancia_hamming(solucion1, solucion2):
    """
    Calcula la distancia de Hamming entre dos puntos de referencia.

    Parámetros:
    ----------
    solucion1 (lista de ints): solucion representada con un arreglo.
    solucion2 (lista de ints): solucion representada con un arreglo.

    Returns:
    ------
    distancia (int): La distancia de Hamming entre los dos puntos de referencia.
    """
    
    distancia = 0
    for i in range(len(solucion1)):
        if solucion1[i] != solucion2[i]:
            distancia += 1
    return distancia

def seleccionar_mejores_soluciones(distancias, conjunto_referencia, tam_conjunto):
    """
    Selecciona las mejores soluciones de una población para mantener la diversidad.

    Parámetros:
    ----------
    distancias (lista de lista de floats): matriz de distancias entre las ciudades.
    conjunto_referencia(lista de lista de ints): arreglo con las soluciones a evaluar.
    tam_conjunto (int): cantidad de soluciones en el conjunto de referencia

    Returns:
    ------
    soluciones_seleccionadas (lista de lista de ints): arreglo de soluciones diversas y de mejor costo seleccionadas
    """
    # Metodo de mejora y de construccion de subconjuntos
    soluciones_ordenadas = sorted(conjunto_referencia, key=lambda solucion: calculate_total_distance(solucion, distancias))

    # Seleccionar soluciones adicionales para mantener la diversidad
    soluciones_diversas = []
    for solucion in soluciones_ordenadas:
        if not soluciones_diversas:
            soluciones_diversas.append(solucion)
            continue

        diverso = True
        for solucion_diversa in soluciones_diversas:
            distancia = distancia_hamming(solucion, solucion_diversa)
            if distancia <= tam_conjunto / 3:  # Umbral de diversidad
                diverso = False
                break

        if diverso:
            soluciones_diversas.append(solucion)


    # Combinar las mejores soluciones por costo y las diversas
    if len(soluciones_diversas) < tam_conjunto*3//4:
        soluciones_seleccionadas = soluciones_diversas + soluciones_ordenadas[:tam_conjunto - len(soluciones_diversas) + 1]
    else:
        soluciones_seleccionadas = soluciones_ordenadas[:tam_conjunto//4] + soluciones_diversas[:(tam_conjunto*3//4)+1]

    return soluciones_seleccionadas

def path_relinking(distance_matrix, solucion_inicial, solucion_guia, conjunto_referencia):
    """
    Realiza el re-enlazado de caminos desde la solucion inicial hasta la solucion guia.

    Parámetros:
    ----------
        distance_matrix (lista de listas de floats): Matriz de distancias entre ciudades.
        solucion_inicial (lista de ints): Solución inicial.
        solucion_guia (lista de ints): Solución guía.
        conjunto_referencia (lista de listas de ints): Conjunto de referencia.

    Returns:
    ------
        mejor_solucion (lista de ints): Mejor solución encontrada por path-relinking.
    """
    
    solucion_actual, mejor_solucion = solucion_inicial.copy(), solucion_inicial.copy()
    menor_distancia = calculate_total_distance(solucion_inicial,distance_matrix)

    while solucion_actual != solucion_guia:
        
        # Encuentra la mejor solución en el vecindario de la solucion
        # Se utiliza 1-swap como vecindad
        mejor_solucion_vecindad = obtener_mejor_solucion_vecindad(distance_matrix,
                                                                  solucion_actual,
                                                                  conjunto_referencia)
        
        # No hay mejores soluciones en la vecindad al aplicar 1-swap
        if mejor_solucion_vecindad == solucion_actual:
            break

        # Actualiza la mejor solución y su costo si la solucion actual mejora
        # caso contrario, se detiene el re-enlazado
        if calculate_total_distance(mejor_solucion_vecindad,distance_matrix) < menor_distancia:
            mejor_solucion, menor_distancia = mejor_solucion_vecindad, calculate_total_distance(mejor_solucion_vecindad,distance_matrix)
        else:
            break

        # Actualiza la solución actual
        solucion_actual = mejor_solucion_vecindad

    return mejor_solucion

def obtener_mejor_solucion_vecindad(distance_matrix, solucion, conjunto_referencia):
    """
    Encuentra la mejor solución en la vecindad restringida de solucion utilizando 1-swap.

    Parámetros:
    ----------
        solucion (lista de ints): Solución actual.

    Returns:
    ------
        mejor_solucion (lista de ints): Mejor solución encontrada en la vecindad.
    """
    mejor_solucion = solucion.copy()
    mejor_costo = calculate_total_distance(solucion,distance_matrix)
    # Se verifican las soluciones que se encuentran en el conjunto de referencia,
    # que estan en la vecindad de solucion
    for i in conjunto_referencia:
        if distancia_hamming(solucion,i) != 2:
            continue
        if mejor_costo > calculate_total_distance(i,distance_matrix):
            mejor_solucion = i
            mejor_costo = calculate_total_distance(i,distance_matrix)

    return mejor_solucion

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

def run_scatter_search(cities_coords, 
                       distance_matrix, 
                       max_iteraciones, 
                       tam_conjunto, 
                       porcentaje_re_enlazado, 
                       nombre, 
                       save_every_5_iter=False,
                       crossover_method="triple",
                       mutation_method="edge_recombination",
                       crossover_rate=0.8,
                       mutation_rate=0.2):
    """
    Ejecuta el algoritmo Scatter Search para el problema TSP.

    Parámetros:
    ----------
    cities_coords (lista de lista de floats): Una lista de listas que contiene las coordenadas de las ciudades.
    distance_matrix (lista de lista de floats): Una matriz de distancias entre las ciudades.
    max_iteraciones (int): El número máximo de iteraciones.
    tam_conjunto: Cantidad de elementos en el conjunto de referencia.
    porcentaje_re_enlazado: El porcentaje de pares de puntos de referencia para re-enlazado.
    save_every_10_iter: Guardar la mejor solución cada 10 iteraciones.
    crossover_method: Método de cruce a utilizar.
    mutation_method: Método de mutación a utilizar.
    crossover_rate: Tasa de cruce.
    mutation_rate: Tasa de mutación.

    Returns:
    ----------
    conjunto_referencia (lista de lista de ints): Conjunto de referencia final
    """

    # Generar el conjunto de referencia inicial
    conjunto_referencia = initial_population(range(len(cities_coords)), tam_conjunto)
    cities_names = [i for i in range(len(distance_matrix))]

    for iter in range(max_iteraciones):
    
        if iter == 0:
            selected_solutions = conjunto_referencia
        
        random.shuffle(selected_solutions)
        aptitude_probabilities = aptitude_probability(
            distance_matrix, selected_solutions
        )

        # Selecciona los padres
        parents_list = [
            roulette_selection(selected_solutions, aptitude_probabilities)
            for _ in range(int(crossover_rate * tam_conjunto))
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
            random.shuffle(selected_solutions)
            
            # Ejecutar re-enlazado de caminos
            if random.random() < porcentaje_re_enlazado:
                offspring_relinked = path_relinking(distance_matrix, offspring, random.shuffle(offspring), selected_solutions)
                if offspring_relinked != offspring:
                    evolved_offspring.append(offspring_relinked)

        evolved_offspring += parents_list

        selected_solutions = seleccionar_mejores_soluciones(distance_matrix, 
                                                            selected_solutions + evolved_offspring, 
                                                            tam_conjunto)
        
        # Guardar las soluciones cada 10 iteraciones
        if save_every_5_iter and ((iter+1)%5 == 0 or iter == 0):
            
            distancias_soluciones = []
            for i in range(tam_conjunto):
                distancias_soluciones.append(calculate_total_distance(selected_solutions[i],distance_matrix))

            index_minimum = np.argmin(distancias_soluciones)
            minimum_distance = min(distancias_soluciones)
            
            print(f"Iteración {iter+1} - Menor distancia: {minimum_distance}")

            shortest_path = selected_solutions[index_minimum].copy()
            shortest_path.append(shortest_path[0])
            plot_path(cities_coords, 
                    shortest_path, 
                    minimum_distance, 
                    title=f"scatter_search_iter{iter+1}_tam{tam_conjunto}_re%{porcentaje_re_enlazado}", 
                    display_graph = False,
                    route=f"scatter-search/{nombre}")

    return selected_solutions

# Parámetros del algoritmo
#tam_conj_ref = [40,60,100]  # Tamaño de la población
tam_conj_ref = [10,20,30]  # Tamaño de la población
#max_iteraciones = [500, 1000, 2000]  # Número máximo de iteraciones
max_iteraciones = [10,20,30]  # Número máximo de iteraciones
porcentaje_re_enlazado = [0.1]  # Porcentaje de pares de puntos de referencia para re-enlazado
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

# Ciclo para obtener los datos de las ciudades y ejecutar la busqueda dispersa
# Se ejecuta la busqueda dispersa para las primeras 5 ciudades de la lista cities_names
for i in [0,1,2,3,4]:
    
    # Se obtienen las coordenadas de las ciudades
    cities_coords = obtener_ciudades(f"../../doc/Benchmarks/{cities_names[i]}.tsp")

    nombre = cities_names[i]

    # Se crea el archivo txt donde se almacenaran los resultados
    # de la ciudad, si ya existe, se sobreescribe
    with open(f"./solutions/scatter_search/{cities_names[i]}.txt", "w") as text_file:
        text_file.write(f"Running scatter search with {cities_names[i]} data \n\n")

    # Se calcula la matriz de distancias
    distance_matrix = np.array(calcular_distancia(cities_coords))

    # Guardar imagenes de la mejor solucion cada 100 generaciones
    # Las imagenes se guardan actualmente en la carpeta de imagenes
    # ubicada en el directorio del proyecto
    save_every_5_iter = True
    
    # Se ejecuta para cada ciudad la busqueda dispersa
    iter = 1
    for j in range(len(tam_conj_ref)):
        for k in range(len(max_iteraciones)):
            for l in range(len(porcentaje_re_enlazado)):
                
                print(f"\nRunning scatter search for {cities_names[i]} (iter {iter}/{len(tam_conj_ref)*len(max_iteraciones)*len(porcentaje_re_enlazado)})")
                print(f"Tam. conjunto de referencia: {tam_conj_ref[j]}")
                print(f"Cantidad de iteraciones: {max_iteraciones[k]}")                
                print(f"Re-link %: {porcentaje_re_enlazado[l]}")
    
                ## Busqueda dispersa
                ss_solution = run_scatter_search(cities_coords, 
                                                distance_matrix, 
                                                max_iteraciones[k],
                                                tam_conj_ref[j],
                                                porcentaje_re_enlazado[l],
                                                nombre,
                                                save_every_5_iter
                                                )

                # Al finalizar el algoritmo memetico, se tiene una poblacion de soluciones
                # Se calcula la distancia total de cada solucion y se selecciona la mejor
                population_dist = []
                for z in range(tam_conj_ref[j]):
                    population_dist.append(calculate_total_distance(ss_solution[z],distance_matrix))

                index_minimum = np.argmin(population_dist)
                shortest_path = ss_solution[index_minimum]
                minimum_distance = min(population_dist)

                # Se escribe la informacion de la mejor solucion en un archivo txt
                with open(f"./solutions/scatter_search/{cities_names[i]}.txt", "a") as text_file:
                    text_file.write(f"Ref. set size: {tam_conj_ref[j]}\n")
                    text_file.write(f"Num iterations: {max_iteraciones[k]}\n")                
                    text_file.write(f"Re-link %: {porcentaje_re_enlazado[l]}\n")
                    text_file.write(f"minimum_distance = {minimum_distance}\n")
                    text_file.write(f"avg_distance = {np.mean(population_dist)}\n")
                    text_file.write("---------------------------------------------\n\n")
                print(f"saved solution data in ./solutions/scatter_search/{cities_names[i]}.txt")
                iter += 1
