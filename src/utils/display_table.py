import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from utils.file_names import FILE_NAMES, LABEL_NAMES
import numpy as np

def display_table(cols, data, city):

    data = np.transpose(data)

    col_labels = [LABEL_NAMES[name] for name in cols]
    rows = ["Distancia\nTotal", "Tiempo de\n ejecucion", "Grafo"]
     
    # Configurar el tamaño de las celdas de la tabla
    table_height = 1 # Altura de la tabla en pulgadas
    table_width = 1  # Ancho de la tabla en pulgadas
    cell_width = table_width / (len(cols))
    cell_height = table_height / (len(rows) + 1)

    fig, ax = plt.subplots(figsize=(19.2,10.8))
    # print(fig, ax)
    ax.axis('off')
    # ax.axis()

    # Agregar la tabla
    table = ax.table(
        cellText=data,
        rowLabels=rows,
        rowLoc = "right",
        colLabels=col_labels,
        loc='center',
        cellLoc='center',
        bbox = [0,0,1,1]
    )

    for i, name in enumerate(cols):

        x = cell_width/2 + (i) * cell_width
        y =  cell_height/2
        image = f"../img/{FILE_NAMES[name]}{city}.png"
        ab = AnnotationBbox(OffsetImage(plt.imread(image), zoom=0.25), (x,y), frameon=False, xycoords='axes fraction')
        ax.add_artist(ab)

    table.auto_set_font_size(False)
    table.set_fontsize(14)

    plt.suptitle(city, y=0.95, fontsize=14, fontweight='bold')
    plt.savefig(f"../img/table_{city}.png")
    plt.show()
