# "Comandante Cody... el momento que estábamos esperando ha llegado. Ejecute la Orden 66"
def usar_la_fuerza(mochila, indice=0, conteo=0):
    # Mochila :p
    if indice >= len(mochila):
        return False, conteo

    objeto_actual = mochila[indice]
    print("Sacando objeto:", objeto_actual)

    if objeto_actual == "sable de luz":
        return True, conteo + 1

    return usar_la_fuerza(mochila, indice + 1, conteo + 1)


# Mochila del Jedi
mochila = [
    "comida",
    "capa jedi",
    "sable de luz",
    "agua",
]

encontrado, cantidad = usar_la_fuerza(mochila)

if encontrado:
    print("Sable encontrado.")
    print("Cantidad de objetos:", cantidad)
else:
    print("No se encontró sable de luz.")
    print("Cantidad de objetos:", cantidad)
    # "Luminosos seres somos, no esta cruda materia"