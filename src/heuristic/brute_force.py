# CI5652 - Diseño de Algoritmos II
# Proyecto Traveling Salesman Problem - Corte 1
# Integrantes:
# Abel Zavaleta,
# Alejandro Meneses,
# Roberto Gamboa, 16-10394

from itertools import permutations
import numpy as np


def traveling_salesman_problem(distances):
    """
    Método exacto para la resolución del problema del agente viajero (TSP).
    
    Este método utiliza la fuerza bruta para encontrar el camino de costo mínimo.
    Genera todas las permutaciones posibles de los nodos y calcula el costo de
    recorrer todos los nodos en el orden dado por cada permutación.
    
    Parámetros:
    ----------

    distances (list of list of int/float): Matriz de distancias entre los nodos
                                           del problema (distances[i][j]
                                           representa la distancia del nodo i
                                           al nodo j).
    
    Return:
    ------

    tuple: Una tupla que contiene:
           - min_distance (int/float): El costo mínimo del camino encontrado.
           - min_path (tuple): El camino (permutación de nodos) de costo mínimo.
    
    Complejidad de tiempo:
    O(n!) donde n es la cantidad de nodos, debido a que evalúa todas las
    permutaciones posibles.
    """
    cantidad_nodos = len(distances)
    min_path = None
    min_distance = float("inf")

    for path in permutations(range(cantidad_nodos)):
        distance = sum(distances[path[i - 1]][path[i]] for i in range(cantidad_nodos))
        if distance < min_distance:
            min_distance = distance
            min_path = path
            # print(f"current min path: {min_path}, current min distance: {min_distance}")

    return min_distance, min_path


if __name__ == "__main__":

    distances = np.array(
        [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]
    )
    distancia, ruta = traveling_salesman_problem(distances)
    print("Solución encontrada:")
    print(f"Distancia minima: {distancia}, Ruta: {ruta}")

    # Ejemplo con matriz de distancias entre 12 ciudades de Alemania
    # (tarda bastante tiempo en ejecutarse)
    # obtenido de: https://medium.com/@marioskokmotos2/the-travelling-salesman-problem-an-implementation-in-python-d2b87e48b9d9
    # Nodos:
    # 0 — Augsburg, 1 — Munich, 2 — Stuttgart,
    # 3 — Nuremberg, 4 — Leipzig, 5 — Dresden,
    # 6 — Berlin, 7 — Hanover, 8 — Bremen,
    # 9 — Hamburg, 10 — Cologne, 11 — Frankfurt
    # Costo de la solucion: 1821; camino: 0 - 2 - 11 - 10 - 7 - 8 - 9 - 6 - 5 - 4 - 3 - 1
    """dist2 = np.array([
        [0,57,133,122,347,362,495,452,543,578,404,250],
	    [57,0,188,144,356,355,498,483,577,605,449,298],
	    [133,188,0,157,365,412,511,402,480,534,289,153],
	    [122,144,157,0,225,258,374,338,433,461,337,187],
	    [347,356,365,225,0,99,150,215,311,295,380,294],
	    [362,355,412,258,99,0,165,312,406,380,473,372],
	    [495,498,511,374,150,165,0,250,316,255,477,422],
	    [452,483,402,338,215,312,250,0,100,135,245,257],
	    [543,577,480,433,311,406,316,100,0,95,270,330],
	    [578,605,534,461,295,380,255,135,95,0,355,392],
	    [404,449,289,337,380,473,477,245,270,355,0,150],
	    [250,298,153,187,294,372,422,257,330,392,150,0]
	])
    distancia, ruta = traveling_salesman_problem(dist2)
    print("Solución encontrada:")
    print(f"Distancia minima: {distancia}, Ruta: {ruta}")"""
