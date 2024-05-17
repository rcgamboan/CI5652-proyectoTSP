from utils.graficar import graficar_ciudades, graficar_recorrido


# Implementacion de un metodo exacto para TSP 
# usando la heuristica del vecino mas cercano (Nearest Neighbour).
# Recibe una matriz de distancias entre los nodos del problema.
# Retorna el camino de costo minimo y su costo asociado.
# Para resolver el problema, parte de un nodo inicial y en cada paso
# selecciona el nodo mas cercano que no haya sido visitado.
# Este proceso se repite hasta visitar todos los nodos.
# Tiempo de ejecución: O(n^2) donde n es la cantidad de nodos.
def nearest_neighbour(matriz_distancia, ciudades, nodo_inicial = 0, guardar = False):
    
    cantidad_nodos = len(matriz_distancia)
    # Inicializa la ruta con el nodo inicial.
    ruta = [nodo_inicial]  
    # Inicializa el conjunto de nodos visitados.
    visitados = set([nodo_inicial])

    iter = 0
    # Se visitan todos los nodos, en cada iteración se selecciona el nodo más cercano.
    while len(visitados) < cantidad_nodos:  
        distancia_min = float('inf')
        for i in range(cantidad_nodos):
            # Se revisan todos los nodos aun no visitados 
            # y se obtiene el nodo que se encuentre más cerca
            if i not in visitados and matriz_distancia[ruta[-1]][i] < distancia_min:
                distancia_min = matriz_distancia[ruta[-1]][i]
                sig_nodo = i
        # El nodo más cercano se agrega al recorrido y se marca como visitado
        ruta.append(sig_nodo)
        visitados.add(sig_nodo)
        if guardar:
            graficar_recorrido(ruta, ciudades, f"NN iter{iter}",False)
        iter+=1

    # Agrega el nodo inicial al final de la ruta para completar el ciclo.
    ruta.append(nodo_inicial)
    # Calcula la distancia total de la ruta.
    distancia_total = sum(matriz_distancia[ruta[i-1]][ruta[i]] for i in range(cantidad_nodos+1))

    return distancia_total, ruta

# Heurística del vecino más cercano con mejor inicio, se ejecuta
# nearest_neighbour para cada nodo inicial y se selecciona la mejor solución.
# Tiempo de ejecución: O(n^3)
def nearest_neighbour_mejor_inicio(matriz_distancia, ciudades):
    distancia_min = float('inf')
    mejor_ruta = None
    for i in range(len(matriz_distancia)):
        distancia, ruta = nearest_neighbour(matriz_distancia, ciudades, i)
        if distancia < distancia_min:
            distancia_min = distancia
            mejor_ruta = ruta
    return distancia_min, mejor_ruta