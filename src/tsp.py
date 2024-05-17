# CI5652 - Diseño de Algoritmos II
# Proyecto Traveling Salesman Problem - Corte 1
# Integrantes:
    # Abel Zavaleta, 
    # Alejandro Meneses, 
    # Roberto Gamboa, 16-10394 

from utils.graficar import graficar_ciudades, graficar_recorrido
from utils.calcular_distancia import calcular_distancia, calcular_costo_ruta
from utils.leer_archivo import obtener_ciudades, obtener_mejor_ruta
from heuristic.greedy import greedy_insertion, greedy_insertion_mejor_inicio
from heuristic.nearest_neighbour import nearest_neighbour, nearest_neighbour_mejor_inicio

if __name__ == "__main__":
    
    # cities = [ "berlin52", "ch130", "pcb442", "pr1002", "tsp225"]
    cities = [ "berlin52"]

    for currentCity in cities:

        nodes = obtener_ciudades(f"../doc/Benchmarks/{currentCity}.tsp")
        best_tour = obtener_mejor_ruta(f"../doc/Benchmarks/{currentCity}.opt.tour")

        #Calculamos las distacion entre nodos y calculamos el costo de la mejor ruta del bechnmark
        distance_matrix = calcular_distancia(nodes)
        best_distance_tour = calcular_costo_ruta(best_tour, distance_matrix)
        
        print(f"Distancia minima posible para {currentCity}: {best_distance_tour}")
        
        show_each_iteration = False

        distance_NN, tour_NN = nearest_neighbour(distance_matrix, nodes, 0, show_each_iteration)
        print("\nNearest Neighbour")
        print(f"Distancia total: {round(distance_NN,2)}")
        
        distance_NN_BS, tour_NN_BS = nearest_neighbour_mejor_inicio(distance_matrix, nodes)    
        print("\nNearest Neighbour mejor inicio")
        print(f"Distancia total: {round(distance_NN_BS,2)}")

        distance_GI, tour_GI = greedy_insertion(distance_matrix, nodes, 0, show_each_iteration)
        print("\nGreedy Insertion")
        print(f"Distancia total: {round(distance_GI,2)}")

        distance_GI_BS, tour_GI_BS = greedy_insertion_mejor_inicio(distance_matrix, nodes)
        print("\nGreedy Insertion mejor inicio")
        print(f"Distancia total: {round(distance_GI_BS,2)}")

        save_graph = True
        show_on_screen = True
        if save_graph:
            graficar_ciudades(nodes, currentCity ,show_on_screen)
            graficar_recorrido(best_tour, nodes, f"mejor_ruta_{currentCity}", show_on_screen)
            graficar_recorrido(tour_NN, nodes, f"nearest_neighbour_{currentCity}", show_on_screen)
            graficar_recorrido(tour_NN_BS, nodes, f"nearest_neighbour_mejor_inicio_{currentCity}", show_on_screen)
            graficar_recorrido(tour_GI, nodes, f"greedy_insertion_{currentCity}", show_on_screen)
            graficar_recorrido(tour_GI_BS, nodes, f"greedy_insertion_mejor_inicio_{currentCity}", show_on_screen)
        
        print()
