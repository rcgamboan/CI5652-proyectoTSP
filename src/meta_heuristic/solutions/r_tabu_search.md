# Resultados obtenidos con diferentes algoritmos de búsqueda: busqueda local, búsqueda Iterativa y búsqueda tabú
| Instancia | Mejor Distancia | Algoritmo | Tiempo | Tipo de Búsqueda |
|-----------|-----------------|-----------|--------|------------------|
| berlin52  | 7544.37         | N/A       | N/A    | N/A              |
| berlin52  | 8192.29         | two_opt_random | 0.00244 | Local         |
| berlin52  | 8060.65         | two_opt_nn     | 0.00144 | Local         |
| berlin52  | 8545.14         | two_opt_greedy | 0.00567 | Local         |
| berlin52  | 7875.06         | double_bridge_random | 0.12431 | Iterativa |
| berlin52  | 7619.15         | double_bridge_nn     | 0.13244 | Iterativa |
| berlin52  | 7830.66         | double_bridge_greedy | 0.2009  | Iterativa |
| berlin52  | 8160.9          | tabu_search_random | 0.61319 | Tabú       |
| berlin52  | 7835.71         | tabu_search_nn     | 0.31212 | Tabú       |
| berlin52  | 8274.37         | tabu_search_greedy | 0.30901 | Tabú       |
| ch130     | 6110.86         | N/A       | N/A    | N/A              |
| ch130     | 6347.33         | two_opt_random | 0.01623 | Local         |
| ch130     | 6741.95         | two_opt_nn     | 0.01531 | Local         |
| ch130     | 6685.54         | two_opt_greedy | 0.07311 | Local         |
| ch130     | 6172.78         | double_bridge_random | 1.78324 | Iterativa |
| ch130     | 6217.98         | double_bridge_nn     | 0.84097 | Iterativa |
| ch130     | 6203.85         | double_bridge_greedy | 2.03749 | Iterativa |
| ch130     | 6553.21         | tabu_search_random | 15.63759 | Tabú      |
| ch130     | 6456.14         | tabu_search_nn     | 6.1815  | Tabú      |
| ch130     | 6706.1          | tabu_search_greedy | 5.28071 | Tabú      |
| tsp225    | 3859            | N/A       | N/A    | N/A              |
| tsp225    | 4360.89         | two_opt_random | 0.06248 | Local         |
| tsp225    | 4176.95         | two_opt_nn     | 0.04638 | Local         |
| tsp225    | 4242.66         | two_opt_greedy | 0.36395 | Local         |
| tsp225    | 4017.71         | double_bridge_random | 6.97517 | Iterativa |
| tsp225    | 4014.25         | double_bridge_nn     | 4.31549 | Iterativa |
| tsp225    | 3970.86         | double_bridge_greedy | 7.49365 | Iterativa |
| tsp225    | 4057.71         | tabu_search_random | 134.65494 | Tabú      |
| tsp225    | 3965.43         | tabu_search_nn     | 45.16452 | Tabú      |
| tsp225    | 4151.27         | tabu_search_greedy | 43.55368 | Tabú      |
