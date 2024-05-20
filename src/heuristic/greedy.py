from utils.graficar import graficar_ciudades, graficar_recorrido


def greedy_insertion(matriz_distancia, ciudades, show_iterations = False, current_city = "", nodo_inicial=0):
    """
    Heurística Greedy Insertion (también llamada cheapest insertion) para la
    resolución del problema del agente viajero (TSP).

    El método comienza desde un nodo inicial y, en cada paso, selecciona el nodo
    que, al ser insertado en la ruta actual, minimiza el aumento de la
    distancia total de la ruta.
    
    Parámetros:
    matriz_distancia ([[int/float]]): Matriz de distancias entre los nodos del
                                      problema. (matriz_distancia[i][j]
                                      representa la distancia del nodo i al nodo j).
    ciudades (list): Lista de nombres o identificadores de las ciudades (nodos).
    nodo_inicial (int): Nodo inicial desde el cual comenzar la ruta. Por defecto es 0.
    guardar (bool): Si es True, genera una imagen por iteración mostrando cómo
                    se agregan los nodos a la ruta.
    
    Return:
    tuple: Una tupla que contiene:
           - distancia_total (int/float): El costo total de la ruta hallada.
           - ruta (list): La secuencia de nodos en la ruta encontrada.
    """

    cantidad_nodos = len(matriz_distancia)
    ruta = [nodo_inicial, nodo_inicial]
    no_visitados = set(range(len(matriz_distancia))) - {nodo_inicial}
    iter = 0
    while no_visitados:
        # Encuentra el nodo no visitado y el lugar donde insertarlo en la ruta,
        # de manera que se minimice el aumento de la distancia.
        sig_nodo, posicion_insertar = min(
            ((node, i) for node in no_visitados for i in range(1, len(ruta))),
            key=lambda x: matriz_distancia[ruta[x[1] - 1]][x[0]]
            + matriz_distancia[x[0]][ruta[x[1]]]
            - matriz_distancia[ruta[x[1] - 1]][ruta[x[1]]],
        )
        ruta.insert(posicion_insertar, sig_nodo)
        no_visitados.remove(sig_nodo)
        if show_iterations:
            # Genera una imagen por iteracion,
            # mostrando como se van agregando los nodos a la ruta.
            graficar_recorrido(
                ruta, 
                ciudades,
                f"greedy/{current_city}" , 
                f"{current_city}_greedy_tour_iter_{iter}", 
                False
            )
        iter += 1

    # Calcula la distancia total de la ruta
    distancia_total = sum(
        matriz_distancia[ruta[i - 1]][ruta[i]] for i in range(cantidad_nodos + 1)
    )

    return distancia_total, ruta


def greedy_insertion_mejor_inicio(matriz_distancia, ciudades):
    """
    Ejecuta la heurística greedy insertion para cada nodo inicial
    posible y selecciona la mejor solución encontrada.

    Parámetros:
    matriz_distancia ([[int/float]]): Matriz de distancias entre los nodos del
                                      problema (matriz_distancia[i][j]
                                      representa la distancia del nodo i al
                                      nodo j).
    ciudades (list): Lista de nombres o identificadores de las ciudades o nodos.

    Retorna:
    tuple: Una tupla que contiene:
           - min_distance (int/float): La distancia mínima de la mejor ruta encontrada.
           - best_path (list): La mejor ruta (lista de nodos) encontrada.
    """
    min_distance = float("inf")
    best_path = None
    for i in range(len(matriz_distancia)):
        distance, path = greedy_insertion(matriz_distancia, ciudades, i, False)
        if distance < min_distance:
            min_distance = distance
            best_path = path
    return min_distance, best_path
