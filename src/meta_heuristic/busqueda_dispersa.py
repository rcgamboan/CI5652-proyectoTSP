import random
import numpy as np
from iteration_utilities import random_permutation

import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.calcular_distancia import calcular_distancia, calculate_total_distance
from utils.leer_archivo import obtener_ciudades
from utils.graficar import plot_path


def obtener_conjunto_inicial(cities_list, tam_conjunto):
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


def obtener_solucion_diversa(solucion):
    """
    Genera una nueva solución diversa mediante la inversion de parte del recorrido.

    Parámetros:
    ----------
    solucion (lista de ints): La solución actual.

    Returns:
    ------
    solucion_diversa (lista de ints): Una nueva solución diversa respecto a la solucion de entrada.
    """
    i1, i2 = sorted(random.sample(range(len(solucion)), 2))
    solucion_diversa = solucion.copy()
    solucion_diversa[i1:i2] = solucion_diversa[i1:i2][::-1]
    return solucion_diversa


def reenlazar_camino(ruta):
    """
    Re-enlaza dos ciudades de una ruta.

    Parámetros:
    ----------
    ruta (lista de ints): Ruta a ser re-enlazada.

    Returns:
    ------
    ruta (lista de ints): Ruta re-enlazada.
    """
    num_ciudades = len(ruta)
    i, j = random.sample(range(num_ciudades), 2)
    ruta[i], ruta[j] = ruta[j], ruta[i]
    return ruta


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
    soluciones_ordenadas = sorted(
        conjunto_referencia,
        key=lambda solucion: calculate_total_distance(solucion, distancias),
    )

    # Seleccionar soluciones adicionales para mantener la diversidad
    soluciones_diversas = []
    for solucion in soluciones_ordenadas:
        if not soluciones_diversas:
            soluciones_diversas.append(solucion)
            continue

        diverso = True
        for solucion_diversa in soluciones_diversas:
            distancia = distancia_hamming(solucion, solucion_diversa)
            if distancia <= tam_conjunto / 2:  # Umbral de diversidad
                diverso = False
                break

        if diverso:
            soluciones_diversas.append(solucion)

    # Combinar las mejores soluciones por costo y las diversas
    if len(soluciones_diversas) < tam_conjunto * 3 // 4:
        soluciones_seleccionadas = (
            soluciones_diversas
            + soluciones_ordenadas[: tam_conjunto - len(soluciones_diversas)]
        )
    else:
        soluciones_seleccionadas = (
            soluciones_ordenadas[: tam_conjunto // 4]
            + soluciones_diversas[: tam_conjunto * 3 // 4]
        )

    return soluciones_seleccionadas


def run_scatter_search(
    cities_coords,
    distance_matrix,
    max_iteraciones,
    tam_conjunto,
    porcentaje_re_enlazado,
    nombre,
    save_every_100_iter=False,
):
    """
    Ejecuta el algoritmo Scatter Search para el problema TSP.

    Parámetros:
    ----------
    cities_coords (lista de lista de floats): Una lista de listas que contiene las coordenadas de las ciudades.
    distance_matrix (lista de lista de floats): Una matriz de distancias entre las ciudades.
    max_iteraciones (int): El número máximo de iteraciones.
    tam_conjunto: Cantidad de elementos en el conjunto de referencia.
    porcentaje_re_enlazado: El porcentaje de pares de puntos de referencia para re-enlazado.
    save_every_100_iter: Guardar la mejor solución cada 100 iteraciones.

    Parámetros:
    ----------
    conjunto_referencia (lista de lista de ints): Conjunto de referencia final
    """

    # Generar el conjunto de referencia inicial
    conjunto_referencia = obtener_conjunto_inicial(
        range(len(cities_coords)), tam_conjunto
    )

    for iter in range(max_iteraciones):

        # Metodo de generacion de soluciones
        nuevo_conjunto = []
        for solucion in conjunto_referencia:
            # Generar soluciones diversas respecto a la actual
            solucion_diversa = obtener_solucion_diversa(solucion)
            nuevo_conjunto.append(solucion_diversa)

            # Re-enlazado de caminos
            if random.random() < porcentaje_re_enlazado:
                solucion_re_enlazada = reenlazar_camino(solucion)
                nuevo_conjunto.append(solucion_re_enlazada)

        # Seleccionar las mejores soluciones y combinarlas con las mas diversas
        conjunto_referencia = seleccionar_mejores_soluciones(
            distance_matrix, conjunto_referencia + nuevo_conjunto, tam_conjunto
        )

        if save_every_100_iter and ((iter + 1) % 100 == 0 or iter == 0):

            total_dist_all_individuals = []
            for i in range(tam_conjunto):
                total_dist_all_individuals.append(
                    calculate_total_distance(conjunto_referencia[i], distance_matrix)
                )

            index_minimum = np.argmin(total_dist_all_individuals)
            minimum_distance = min(total_dist_all_individuals)

            print(f"Iteración {iter+1} - Menor distancia: {minimum_distance}")

            shortest_path = conjunto_referencia[index_minimum].copy()
            shortest_path.append(shortest_path[0])
            plot_path(
                cities_coords,
                shortest_path,
                minimum_distance,
                title=f"scatter_search_iter{iter+1}_tam{tam_conj_ref}_re%{porcentaje_re_enlazado}",
                display_graph=False,
                route=f"scatter-search/{nombre}",
            )

    return conjunto_referencia


# Parámetros del algoritmo
tam_conj_ref = [40, 60, 100]  # Tamaño de la población
max_iteraciones = [500, 1000, 2000]  # Número máximo de iteraciones
porcentaje_re_enlazado = [
    0.2
]  # Porcentaje de pares de puntos de referencia para re-enlazado

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

# Ciclo para obtener los datos de las ciudades y ejecutar la busqueda dispersa
# Se ejecuta la busqueda dispersa para las primeras 5 ciudades de la lista cities_names
for i in range(1):
    # Se obtienen las coordenadas de las ciudades
    cities_coords = obtener_ciudades(f"../../doc/Benchmarks/{cities_names[i]}.tsp")

    nombre = cities_names[i]

    # Se crea el archivo txt donde se almacenaran los resultados
    # de la ciudad, si ya existe, se sobreescribe
    with open(f"./solutions/scatter_search/{cities_names[i]}.txt", "w") as text_file:
        text_file.write(f"Running scatter search with {cities_names[i]} data \n\n")

    # Se calcula la matriz de distancias
    distance_matrix = np.array(calcular_distancia(cities_coords))

    # Guardar imagenes de la mejor solucion cada 10 generaciones
    # Las imagenes se guardan actualmente en la carpeta de imagenes
    # ubicada en el directorio del proyecto
    save_every_100_iter = True

    # Se ejecuta para cada ciudad la busqueda dispersa
    iter = 1
    for j in range(len(tam_conj_ref)):
        for k in range(len(max_iteraciones)):
            for l in range(len(porcentaje_re_enlazado)):

                print(
                    f"\nRunning scatter search for {cities_names[i]} (iter {iter}/{len(tam_conj_ref)*len(max_iteraciones)*len(porcentaje_re_enlazado)})"
                )
                print(f"Population size: {tam_conj_ref[j]}")
                print(f"Cantidad de iteraciones: {max_iteraciones[k]}")
                print(f"Re-link %: {porcentaje_re_enlazado[l]}")

                ## Busqueda dispersa
                ss_solution = run_scatter_search(
                    cities_coords,
                    distance_matrix,
                    max_iteraciones[k],
                    tam_conj_ref[j],
                    porcentaje_re_enlazado[l],
                    nombre,
                    save_every_100_iter,
                )

                # Al finalizar el algoritmo memetico, se tiene una poblacion de soluciones
                # Se calcula la distancia total de cada solucion y se selecciona la mejor
                population_dist = []
                for z in range(tam_conj_ref[j]):
                    population_dist.append(
                        calculate_total_distance(ss_solution[z], distance_matrix)
                    )

                index_minimum = np.argmin(population_dist)
                shortest_path = ss_solution[index_minimum]
                minimum_distance = min(population_dist)

                # Se escribe la informacion de la mejor solucion en un archivo txt
                with open(
                    f"./solutions/scatter_search/{cities_names[i]}.txt", "a"
                ) as text_file:
                    text_file.write(f"Population size: {tam_conj_ref[j]}\n")
                    text_file.write(f"Num iterations: {max_iteraciones[k]}\n")
                    text_file.write(f"Re-link %: {porcentaje_re_enlazado[l]}\n")
                    text_file.write(f"minimum_distance = {minimum_distance}\n")
                    text_file.write(f"avg_distance = {np.mean(population_dist)}\n")
                    text_file.write("---------------------------------------------\n\n")
                print(
                    f"saved solution data in ./solutions/scatter_search/{cities_names[i]}.txt"
                )
                iter += 1
