import matplotlib.pyplot as plt

# Utilidad para graficar las ciudades en un plano.
def graficar_ciudades(cities, title="Ciudades", mostrar=True):

    plt.style.use("fivethirtyeight")

    plt.scatter(
        [city[0] for city in cities],
        [city[1] for city in cities],
    )

    plt.axis("off")
    plt.title(title)
    plt.savefig(f"../img/{title}.png")
    if mostrar:
        plt.show()
    plt.close()

# Utilidad para graficar el recorrido de las ciudades en un plano.
def graficar_recorrido(path, cities, file_path, file_name, mostrar=False):

    plt.scatter(
        [city[0] for city in cities],
        [city[1] for city in cities],
    )

    plt.plot(
        [cities[path[i]][0] for i in range(len(path))],
        [cities[path[i]][1] for i in range(len(path))],
        c="k",
        linewidth=1,
        zorder=-1,
    )

    plt.title(file_name)

    plt.axis("off")
    plt.savefig(f"../img/{file_path}/{file_name}.png")
    if mostrar:
        plt.show()
    plt.close()

def plot_path(cities_coords, shortest_path,minimum_distance,title="TSP GA", folder="", display_graph=False):

    fig, ax = plt.subplots()
    ax.plot(
        [cities_coords[shortest_path[i]][0] for i in range(len(shortest_path))],
        [cities_coords[shortest_path[i]][1] for i in range(len(shortest_path))],
        '--ko',
        label='Best Route', 
        linewidth=1.5)
    plt.legend()
    
    # Titulo del grafico
    plt.title(label=f"{title}\n Total Distance: {round(minimum_distance, 3)}",
            fontsize=24,
            color="k")

    fig.set_size_inches(16, 12)  
    plt.savefig(f'../../img/{folder}/{title}.png')
    if display_graph:
        plt.show()
    plt.close()
