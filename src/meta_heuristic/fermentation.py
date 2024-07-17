import numpy as np
import random
from pathlib import Path
import sys, os
import time
import signal
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils.calcular_distancia import (
    calcular_distancia,
    calculate_total_distance,
    calcular_costo_ruta,
)
from utils.graficar import graficar_recorrido
from utils.leer_archivo import obtener_ciudades, obtener_mejor_ruta

# Obtiene la ruta del proyecto
PROJECT_DIR = Path(__file__).resolve().parents[2]


def generate_initial_solution(cities):
    """
    Genera una solucion inicial de forma aleatoria
    """
    return random.sample(cities, len(cities))


def evaluate_solutions(population, distance_matrix):
    """
    Evalua las soluciones basada en energia (calidad de la solucion)
    """
    return [
        (solution, calculate_total_distance(solution, distance_matrix))
        for solution in population
    ]


def metabolize_solutions(evaluated_solutions, nutrient_factor):
    """
    Metabolismo: Consumo de nutrientes y producción de energía
    """
    total_energy = sum(1 / distance for _, distance in evaluated_solutions)
    return [
        (solution, (1 / distance) / total_energy * nutrient_factor)
        for solution, distance in evaluated_solutions
    ]


def produce_subproducts(solution):
    """
    Produce subproductos usando operadores 2-opt
    """
    subproduct = solution[:]
    a, b = random.sample(range(len(subproduct)), 2)
    if a > b:
        a, b = b, a
    subproduct[a:b] = reversed(subproduct[a:b])
    return subproduct


def adapt_and_mutate(solution, mutation_rate):
    """
    Adaptacion y mutacion
    """
    if random.random() < mutation_rate:
        a, b = random.sample(range(len(solution)), 2)
        solution[a], solution[b] = solution[b], solution[a]
    return solution


def local_search(solution, distance_matrix):
    """
    Mejor local utilizando el operador 2-opt
    """
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
                if calculate_total_distance(
                    new_solution, distance_matrix
                ) < calculate_total_distance(best, distance_matrix):
                    best = new_solution
                    improved = True
        solution = best
    return best


def fermentation_optimization(
    cities, distance_matrix, iterations, population_size, mutation_rate
):
    """
    Optimizacion por fermentacion
    """
    # Inicializa la población
    population = [
        generate_initial_solution(cities) for _ in range(population_size)
    ]
    best_solution = min(
        population, key=lambda s: calculate_total_distance(s, distance_matrix)
    )
    best_distance = calculate_total_distance(best_solution, distance_matrix)

    for i in range(iterations):
        # Evaluación inicial
        evaluated_solutions = evaluate_solutions(population, distance_matrix)

        # Metabolismo y producción de energía
        nutrient_factor = 1 - (
            i / iterations
        )  # Disminución de nutrientes con el tiempo
        metabolized_solutions = metabolize_solutions(
            evaluated_solutions, nutrient_factor
        )

        # Producción de subproductos
        subproducts = [
            produce_subproducts(solution)
            for solution, _ in metabolized_solutions
        ]

        # Adaptación y mutación
        new_population = [
            adapt_and_mutate(subproduct, mutation_rate)
            for subproduct in subproducts
        ]

        # Aplica la mejora local a la nueva población
        new_population = [
            local_search(solution, distance_matrix)
            for solution in new_population
        ]

        # Evalua la nueva población
        evaluated_new_population = evaluate_solutions(
            new_population, distance_matrix
        )

        # Reemplazo y evolución
        population = [solution for solution, _ in evaluated_new_population]
        current_best = min(
            population,
            key=lambda s: calculate_total_distance(s, distance_matrix),
        )
        current_best_distance = calculate_total_distance(
            current_best, distance_matrix
        )
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
    "sra104815",
]

# Inicializa una lista para almacenar los resultados
results = []


def save_results_to_csv():
    df_results = pd.DataFrame(results)
    # df_results.to_csv(PROJECT_DIR / "results.csv", index=False)
    df_results.to_csv(
        PROJECT_DIR / "img/fermentation/fermentation_results.csv", index=False
    )
    print("Resultados guardados en results.csv")


def signal_handler(sig, frame):
    print("\nInterrupción detectada. Guardando resultados...")
    save_results_to_csv()
    sys.exit(0)


# Configura la señal para capturar Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

for i in range(4):
    # Obtiene las coordenadas de la solucion
    cities_coords = obtener_ciudades(
        PROJECT_DIR / f"doc/Benchmarks/{cities_names[i]}.tsp"
    )

    # Obtiene la matriz de distancias
    distance_matrix = np.array(calcular_distancia(cities_coords))

    # Optimiza la solucion
    start = time.time()
    best_solution, best_distance = fermentation_optimization(
        list(range(len(cities_coords))),
        distance_matrix,
        iterations=10,
        population_size=10,
        mutation_rate=0.1,
    )
    end = time.time()

    # Obtiene el mejor recorrido del benchmark
    best_tour = obtener_mejor_ruta(
        PROJECT_DIR / f"doc/Benchmarks/{cities_names[i]}.opt.tour"
    )

    # Calcula la distancia optima de la instancia
    best_distance_tour = calcular_costo_ruta(best_tour, distance_matrix)

    # Calcula la distancia relativa
    relative_distance = (
        (best_distance - best_distance_tour) / best_distance_tour
    ) * 100

    # Almacena los resultados
    results.append(
        {
            "City": cities_names[i],
            "Best Distance": best_distance,
            "Optimal Distance": best_distance_tour,
            "Relative Distance (%)": relative_distance,
            "Execution Time (s)": end - start,
        }
    )

    print(f"Mejor solución para {cities_names[i]}: {best_solution}")
    print(f"Mejor distancia para {cities_names[i]}: {best_distance}")
    print(f"Tiempo de ejecución: {end - start} segundos\n")

    # Completa el recorrido
    best_solution.append(best_solution[0])

    # Grafica el recorrido
    graficar_recorrido(
        best_solution,
        cities_coords,
        "fermentation",
        f"fermentation_{cities_names[i]}",
        mostrar=True,
    )

# Crea un DataFrame de pandas
df_results = pd.DataFrame(results)

# Guarda los resultados en un archivo CSV
df_results.to_csv(
    PROJECT_DIR / "img/fermentation/fermentation_results.csv", index=False
)

# Muestra la tabla de resultados
print(df_results)
