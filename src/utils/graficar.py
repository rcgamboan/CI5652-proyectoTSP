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
def graficar_recorrido(path, cities, title="Recorrido", mostrar=False):

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

    plt.title(title)

    plt.axis("off")
    plt.savefig(f"../img/{title}.png")
    if mostrar:
        plt.show()
    plt.close()
