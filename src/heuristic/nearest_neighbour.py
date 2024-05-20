from utils.graficar import graficar_ciudades, graficar_recorrido


def nearest_neighbour(matriz_distancia, ciudades, show_iterations = False, current_city = "", nodo_inicial=0):
    """
    Método exacto para la resolución del problema del agente viajero (TSP).

    Este método utiliza la heurística del Vecino Más Cercano para encontrar el
    camino de costo mínimo. Parte de un nodo inicial y, en cada paso, selecciona
    el nodo más cercano que no haya sido visitado aún. Este proceso se repite
    hasta visitar todos los nodos.

    Parámetros:
    ----------

    matriz_distancia ([[int/float]]): Matriz de distancias entre los nodos del
                                      problema.
                                      (matriz_distancia[i][j] representa la
                                      distancia del nodo i al nodo j).
    ciudades (list): Lista de nombres o identificadores de las ciudades o nodos.
    nodo_inicial (int, opcional): Índice del nodo inicial desde el cual comenzar
    la ruta. Por defecto es 0.
    guardar (bool, opcional): Si es True, genera una imagen por iteración
    mostrando cómo se van agregando los nodos a la ruta. Por defecto es False.

    Return:
    ------

    tuple: Una tupla que contiene:
           - distancia_total (int/float): La distancia total de la ruta encontrada.
           - ruta (list): La ruta (lista de nodos) encontrada.

    Complejidad de tiempo: 
    O(n^2) donde n es la cantidad de nodos.
    """

    cantidad_nodos = len(matriz_distancia)
    # Inicializa la ruta con el nodo inicial.
    ruta = [nodo_inicial]
    # Inicializa el conjunto de nodos visitados.
    visitados = set([nodo_inicial])

    iter = 0
    # Se visitan todos los nodos, en cada iteración se selecciona el nodo más cercano.
    while len(visitados) < cantidad_nodos:
        distancia_min = float("inf")
        for i in range(cantidad_nodos):
            # Se revisan todos los nodos aun no visitados
            # y se obtiene el nodo que se encuentre más cerca
            if i not in visitados and matriz_distancia[ruta[-1]][i] < distancia_min:
                distancia_min = matriz_distancia[ruta[-1]][i]
                sig_nodo = i
        # El nodo más cercano se agrega al recorrido y se marca como visitado
        ruta.append(sig_nodo)
        visitados.add(sig_nodo)
        if show_iterations:
            graficar_recorrido(
                ruta, 
                ciudades, 
                f"nn/{current_city}" , 
                f"{current_city}_nn_tour_iter_{iter}", 
                False)
        iter += 1

    # Agrega el nodo inicial al final de la ruta para completar el ciclo.
    ruta.append(nodo_inicial)
    # Calcula la distancia total de la ruta.
    distancia_total = sum(
        matriz_distancia[ruta[i - 1]][ruta[i]] for i in range(cantidad_nodos + 1)
    )

    return distancia_total, ruta


def nearest_neighbour_mejor_inicio(matriz_distancia, ciudades):
    """
    Ejecuta la heurística del vecino más cercano para cada nodo inicial posible
    y selecciona la mejor solución encontrada.

    Parámetros:
    ----------

    matriz_distancia ([[int/float]]): Matriz de distancias entre los nodos del
                                      problema (matriz_distancia[i][j] 
                                      representa la distancia del nodo i al
                                      nodo j).
    ciudades (list): Lista de nombres o identificadores de las ciudades o nodos.

    Return:
    ------

    tuple: Una tupla que contiene:
           - distancia_min (int/float): La distancia mínima de la mejor ruta encontrada.
           - mejor_ruta (list): La mejor ruta (lista de nodos) encontrada.

    Complejidad de tiempo: 
    O(n^3) donde n es la cantidad de nodos.
    """
    distancia_min = float("inf")
    mejor_ruta = None
    for i in range(len(matriz_distancia)):
        distancia, ruta = nearest_neighbour(matriz_distancia, ciudades, i)
        if distancia < distancia_min:
            distancia_min = distancia
            mejor_ruta = ruta
    return distancia_min, mejor_ruta
