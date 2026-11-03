import json
import os
import random


class nodoCola(object):
    def __init__(self, info):
        self.info = info
        self.sig = None


class Cola(object):
    def __init__(self):
        self.frente = None
        self.final = None
        self.tamanio = 0


def arribo(cola, dato):
    nodo = nodoCola(dato)
    if cola.frente is None:
        cola.frente = nodo
    else:
        cola.final.sig = nodo
    cola.final = nodo
    cola.tamanio += 1


def atencion(cola):
    dato = cola.frente.info
    cola.frente = cola.frente.sig
    if cola.frente is None:
        cola.final = None
    cola.tamanio -= 1
    return dato


def cola_vacia(cola):
    return cola.frente is None


class nodoArbol(object):
    def __init__(self, info, dato):
        self.izq = None
        self.der = None
        self.info = info
        self.datos = [dato]


def arbol_vacio(raiz):
    return raiz is None


def insertar_nodo(raiz, clave, dato):
    if raiz is None:
        raiz = nodoArbol(clave, dato)
    elif clave == raiz.info:
        raiz.datos.append(dato)
    elif clave < raiz.info:
        raiz.izq = insertar_nodo(raiz.izq, clave, dato)
    else:
        raiz.der = insertar_nodo(raiz.der, clave, dato)
    return raiz


def buscar(raiz, clave):
    pos = None
    if raiz is not None:
        if raiz.info == clave:
            pos = raiz
        elif clave < raiz.info:
            pos = buscar(raiz.izq, clave)
        else:
            pos = buscar(raiz.der, clave)
    return pos


def inorden(raiz, nodos):
    if raiz is not None:
        inorden(raiz.izq, nodos)
        nodos.append(raiz)
        inorden(raiz.der, nodos)
    return nodos


def por_nivel(raiz):
    resultado = []
    pendientes = Cola()
    if raiz is not None:
        arribo(pendientes, (raiz, 0))
    while not cola_vacia(pendientes):
        nodo, nivel = atencion(pendientes)
        resultado.append((nivel, nodo))
        if nodo.izq is not None:
            arribo(pendientes, (nodo.izq, nivel + 1))
        if nodo.der is not None:
            arribo(pendientes, (nodo.der, nivel + 1))
    return resultado


def cargar_pokemons():
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pokemons.json")
    with open(ruta, "r", encoding="utf-8") as archivo:
        pokemons = json.load(archivo)
    random.shuffle(pokemons)
    raiz_nombre = None
    raiz_numero = None
    raiz_tipo = None
    for pokemon in pokemons:
        raiz_nombre = insertar_nodo(raiz_nombre, pokemon["nombre"].lower(), pokemon)
        raiz_numero = insertar_nodo(raiz_numero, pokemon["numero"], pokemon)
        for tipo in pokemon["tipos"]:
            raiz_tipo = insertar_nodo(raiz_tipo, tipo, pokemon)
    return raiz_nombre, raiz_numero, raiz_tipo

def mostrar_pokemon(pokemon):
    print(f"  Numero: {pokemon['numero']}")
    print(f"  Nombre: {pokemon['nombre']}")
    print(f"  Tipos: {', '.join(pokemon['tipos'])}")
    print(f"  Debilidades: {', '.join(pokemon['debilidades'])}")
    print(f"  Mega evolucion: {'Si' if pokemon['mega'] else 'No'}")
    print(f"  Gigamax: {'Si' if pokemon['gigamax'] else 'No'}")
    print()


def buscar_por_numero(raiz_numero, numero):
    nodo = buscar(raiz_numero, numero)
    if nodo is None:
        print(f"No existe el Pokemon numero {numero}")
    else:
        for pokemon in nodo.datos:
            mostrar_pokemon(pokemon)


def buscar_por_proximidad(raiz_nombre, texto):
    texto = texto.lower()
    encontrados = False
    for nodo in inorden(raiz_nombre, []):
        if texto in nodo.info:
            encontrados = True
            for pokemon in nodo.datos:
                mostrar_pokemon(pokemon)
    if not encontrados:
        print(f"Ningun Pokemon coincide con '{texto}'")


def nombres_por_tipo(raiz_tipo, tipo):
    nodo = buscar(raiz_tipo, tipo)
    pokemons = nodo.datos if nodo is not None else []
    print(f"Pokemons de tipo {tipo}: {len(pokemons)}")
    for pokemon in sorted(pokemons, key=lambda p: p["nombre"]):
        print(f"  {pokemon['nombre']}")


def listado_por_numero(raiz_numero):
    for nodo in inorden(raiz_numero, []):
        for pokemon in nodo.datos:
            print(f"  {pokemon['numero']:>4} - {pokemon['nombre']}")


def listado_por_nombre(raiz_nombre):
    for nodo in inorden(raiz_nombre, []):
        for pokemon in nodo.datos:
            print(f"  {pokemon['nombre']} ({pokemon['numero']})")


def listado_por_nivel_nombre(raiz_nombre):
    nivel_actual = -1
    for nivel, nodo in por_nivel(raiz_nombre):
        if nivel != nivel_actual:
            nivel_actual = nivel
            print(f"Nivel {nivel}:")
        for pokemon in nodo.datos:
            print(f"  {pokemon['nombre']}")


def debiles_frente_a(raiz_nombre, raiz_numero, nombres):
    for nombre in nombres:
        nodo = buscar(raiz_nombre, nombre.lower())
        if nodo is None:
            print(f"{nombre} no esta cargado")
            continue
        tipos_atacante = nodo.datos[0]["tipos"]
        print(f"Debiles frente a {nombre} (tipo/s: {', '.join(tipos_atacante)}):")
        for nodo_numero in inorden(raiz_numero, []):
            pokemon = nodo_numero.datos[0]
            if any(tipo in pokemon["debilidades"] for tipo in tipos_atacante):
                print(f"  {pokemon['nombre']}")
        print()


def cantidad_por_tipo(raiz_tipo):
    for nodo in inorden(raiz_tipo, []):
        print(f"  {nodo.info}: {len(nodo.datos)}")


def contar_mega(raiz_numero):
    return sum(1 for nodo in inorden(raiz_numero, []) if nodo.datos[0]["mega"])


def contar_gigamax(raiz_numero):
    return sum(1 for nodo in inorden(raiz_numero, []) if nodo.datos[0]["gigamax"])


def ejercicio_1():
    print("=" * 60)
    print("EJERCICIO 1 - POKEMONS")
    print("=" * 60)
    raiz_nombre, raiz_numero, raiz_tipo = cargar_pokemons()

    print("\nBusqueda por numero (25):")
    buscar_por_numero(raiz_numero, 25)

    print("Busqueda por proximidad ('bul'):")
    buscar_por_proximidad(raiz_nombre, "bul")

    print("Busqueda por proximidad ('char'):")
    buscar_por_proximidad(raiz_nombre, "char")

    print("Pokemons por tipo:")
    for tipo in ["fantasma", "fuego", "acero", "electrico"]:
        nombres_por_tipo(raiz_tipo, tipo)
        print()

    print("Listado ascendente por numero:")
    listado_por_numero(raiz_numero)

    print("\nListado ascendente por nombre:")
    listado_por_nombre(raiz_nombre)

    print("\nListado por nivel (arbol de nombres):")
    listado_por_nivel_nombre(raiz_nombre)

    print("\nPokemons debiles frente a Jolteon, Lycanroc y Tyrantrum:")
    debiles_frente_a(raiz_nombre, raiz_numero, ["Jolteon", "Lycanroc", "Tyrantrum"])

    print("Cantidad de Pokemons por tipo:")
    cantidad_por_tipo(raiz_tipo)

    print(f"\nPokemons con megaevolucion: {contar_mega(raiz_numero)}")
    print(f"Pokemons con forma gigamax: {contar_gigamax(raiz_numero)}")


if __name__ == "__main__":
    ejercicio_1()
