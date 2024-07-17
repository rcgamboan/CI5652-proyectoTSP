# Graficar el recorrido encontrado por la metaheurística de fermentación
import sys, os
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils.calcular_distancia import (
    calcular_distancia,
    calculate_total_distance,
)

from utils.leer_archivo import obtener_ciudades
from utils.graficar import graficar_recorrido

# Obtiene la ruta del proyecto
PROJECT_DIR = Path(__file__).resolve().parents[2]

berlin52 = [
    47,
    23,
    4,
    5,
    3,
    14,
    37,
    36,
    39,
    38,
    33,
    34,
    35,
    48,
    31,
    44,
    18,
    40,
    7,
    8,
    9,
    42,
    32,
    50,
    10,
    51,
    13,
    12,
    46,
    25,
    26,
    27,
    11,
    24,
    45,
    43,
    15,
    28,
    49,
    19,
    22,
    29,
    1,
    6,
    41,
    20,
    16,
    2,
    17,
    30,
    21,
    0,
]

berlin52_coords = obtener_ciudades(
    PROJECT_DIR / "doc/Benchmarks/berlin52.tsp"
)

# def graficar_recorrido(path, cities, file_path, file_name, mostrar=False):

graficar_recorrido(
    berlin52,
    berlin52_coords,
    "fermentation",
    "fermentation_berlin52",
    mostrar=True,
)
