# CI5652 - Diseño de Algoritmos II
# Proyecto Traveling Salesman Problem - Corte 1
# Integrantes:
    # Abel Zavaleta, 
    # Alejandro Meneses, 
    # Roberto Gamboa, 16-10394 

from utils.graficar import graficar_ciudades, graficar_recorrido
from utils.calcular_distancia import calcular_distancia, calcular_costo_ruta
from utils.leer_archivo import obtener_ciudades, obtener_mejor_ruta

# Implementacion de un metodo exacto para TSP 
# usando la heuristica del vecino mas cercano (Nearest Neighbour).
# Recibe una matriz de distancias entre los nodos del problema.
# Retorna el camino de costo minimo y su costo asociado.
# Para resolver el problema, parte de un nodo inicial y en cada paso
# selecciona el nodo mas cercano que no haya sido visitado.
# Este proceso se repite hasta visitar todos los nodos.
# Tiempo de ejecución: O(n^2) donde n es la cantidad de nodos.
def nearest_neighbour(matriz_distancia, nodo_inicial = 0, guardar = False):
    
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
def nearest_neighbour_mejor_inicio(matriz_distancia):
    distancia_min = float('inf')
    mejor_ruta = None
    for i in range(len(matriz_distancia)):
        distancia, ruta = nearest_neighbour(matriz_distancia, i)
        if distancia < distancia_min:
            distancia_min = distancia
            mejor_ruta = ruta
    return distancia_min, mejor_ruta

# Heuristica Greedy insertion (tambien llamada cheapest insertion)
# Recibe una matriz de distancias entre los nodos del problema.
# Retorna la ruta hallada con el costo minimo y su costo asociado.
# Para resolver el problema, parte de un nodo inicial y en cada paso
# selecciona el nodo que al ser insertado en la ruta minimiza el aumento de la distancia.
def greedy_insertion(matriz_distancia, nodo_inicial = 0, guardar = False):
    cantidad_nodos = len(matriz_distancia)
    ruta = [nodo_inicial, nodo_inicial]
    no_visitados = set(range(len(matriz_distancia))) - {nodo_inicial}
    iter = 0
    while no_visitados:
        # Encuentra el nodo no visitado y el lugar donde insertarlo en la ruta,
        # de manera que se minimice el aumento de la distancia.
        sig_nodo, posicion_insertar = min(((node, i) for node in no_visitados for i in range(1, len(ruta))), key=lambda x: matriz_distancia[ruta[x[1]-1]][x[0]] + matriz_distancia[x[0]][ruta[x[1]]] - matriz_distancia[ruta[x[1]-1]][ruta[x[1]]])
        ruta.insert(posicion_insertar, sig_nodo)
        no_visitados.remove(sig_nodo)
        if guardar:
            # Genera una imagen por iteracion,
            # mostrando como se van agregando los nodos a la ruta.
            graficar_recorrido(ruta, ciudades, f"GI iter{iter}",False)
        iter+=1

    # Calcula la distancia total de la ruta
    distancia_total = sum(matriz_distancia[ruta[i-1]][ruta[i]] for i in range(cantidad_nodos+1))

    return distancia_total, ruta

# Heurística greedy insertion con mejor inicio, se ejecuta
# greedy_insertion para cada nodo inicial y se selecciona la mejor solución.      
def greedy_insertion_mejor_inicio(matriz_distancia):
    min_distance = float('inf')
    best_path = None
    for i in range(len(matriz_distancia)):
        distance, path = greedy_insertion(matriz_distancia, i,False)
        if distance < min_distance:
            min_distance = distance
            best_path = path
    return min_distance, best_path

if __name__ == "__main__":
    
    ciudades = obtener_ciudades('../doc/Benchmarks/berlin52.tsp')
    mejor_ruta = obtener_mejor_ruta('../doc/Benchmarks/berlin52.opt.tour')

    #### Otras ciudades
    #ciudades = obtener_ciudades('../doc/Benchmarks/ch130.tsp')
    #mejor_ruta = obtener_mejor_ruta('../doc/Benchmarks/ch130.opt.tour')
    #ciudades = obtener_ciudades('../doc/Benchmarks/tsp225.tsp')
    #mejor_ruta = obtener_mejor_ruta('../doc/Benchmarks/tsp225.opt.tour')
    #ciudades = obtener_ciudades('../doc/Benchmarks/pcb442.tsp')
    #mejor_ruta = obtener_mejor_ruta('../doc/Benchmarks/pcb442.opt.tour')
    #ciudades = obtener_ciudades('../doc/Benchmarks/pr1002.tsp')
    #mejor_ruta = obtener_mejor_ruta('../doc/Benchmarks/pr1002.opt.tour')

    matriz_distancia = calcular_distancia(ciudades)
    menor_distancia = calcular_costo_ruta(mejor_ruta, matriz_distancia)
    
    print(f"Distancia minima posible: {menor_distancia}")
    
    guardar = False
    distanciaNN, rutaNN = nearest_neighbour(matriz_distancia, 0, guardar)
    print("\nNearest Neighbour")
    print(f"Distancia total: {round(distanciaNN,2)}")
    
    distanciaNNBS, rutaNNBS = nearest_neighbour_mejor_inicio(matriz_distancia)    
    print("\nNearest Neighbour mejor inicio")
    print(f"Distancia total: {round(distanciaNNBS,2)}")

    distanciaGI, rutaGI = greedy_insertion(matriz_distancia,0, guardar)
    print("\nGreedy Insertion")
    print(f"Distancia total: {round(distanciaGI,2)}")

    distanciaGIBS, rutaGIBS = greedy_insertion_mejor_inicio(matriz_distancia)
    print("\nGreedy Insertion mejor inicio")
    print(f"Distancia total: {round(distanciaGIBS,2)}")

    graficar = False
    mostrar_imagenes = False
    if graficar:
        graficar_ciudades(ciudades, "berlin52",mostrar_imagenes)
        graficar_recorrido(mejor_ruta, ciudades, "Mejor Ruta berlin52",mostrar_imagenes)
        graficar_recorrido(rutaNN, ciudades, "Nearest Neighbour",mostrar_imagenes)
        graficar_recorrido(rutaNNBS, ciudades, "Nearest Neighbour mejor inicio",mostrar_imagenes)
        graficar_recorrido(rutaGI, ciudades, "Greedy Insertion",mostrar_imagenes)
        graficar_recorrido(rutaGIBS, ciudades, "Greedy Insertion mejor inicio",mostrar_imagenes)
