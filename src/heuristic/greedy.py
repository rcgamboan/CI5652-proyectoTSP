from utils.graficar import graficar_ciudades, graficar_recorrido


# Heuristica Greedy insertion (tambien llamada cheapest insertion)
# Recibe una matriz de distancias entre los nodos del problema.
# Retorna la ruta hallada con el costo minimo y su costo asociado.
# Para resolver el problema, parte de un nodo inicial y en cada paso
# selecciona el nodo que al ser insertado en la ruta minimiza el aumento de la distancia.
def greedy_insertion(matriz_distancia, ciudades, nodo_inicial=0, guardar=False):
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
        if guardar:
            # Genera una imagen por iteracion,
            # mostrando como se van agregando los nodos a la ruta.
            graficar_recorrido(ruta, ciudades, f"GI iter{iter}", False)
        iter += 1

    # Calcula la distancia total de la ruta
    distancia_total = sum(
        matriz_distancia[ruta[i - 1]][ruta[i]] for i in range(cantidad_nodos + 1)
    )

    return distancia_total, ruta


# Heurística greedy insertion con mejor inicio, se ejecuta
# greedy_insertion para cada nodo inicial y se selecciona la mejor solución.
def greedy_insertion_mejor_inicio(matriz_distancia, ciudades):
    min_distance = float("inf")
    best_path = None
    for i in range(len(matriz_distancia)):
        distance, path = greedy_insertion(matriz_distancia, ciudades, i, False)
        if distance < min_distance:
            min_distance = distance
            best_path = path
    return min_distance, best_path
