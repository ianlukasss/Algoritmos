import math


class Heap(object):
    def __init__(self):
        self.vector = []
        self.tamanio = 0


def heap_vacio(heap):
    return heap.tamanio == 0


def intercambio(heap, i, j):
    heap.vector[i], heap.vector[j] = heap.vector[j], heap.vector[i]


def flotar(heap, hijo):
    while hijo > 0:
        padre = (hijo - 1) // 2
        if heap.vector[hijo][0] < heap.vector[padre][0]:
            intercambio(heap, hijo, padre)
            hijo = padre
        else:
            break


def hundir(heap, padre):
    while True:
        menor = padre
        izq = 2 * padre + 1
        der = izq + 1
        if izq < heap.tamanio and heap.vector[izq][0] < heap.vector[menor][0]:
            menor = izq
        if der < heap.tamanio and heap.vector[der][0] < heap.vector[menor][0]:
            menor = der
        if menor == padre:
            break
        intercambio(heap, padre, menor)
        padre = menor


def arribo_h(heap, dato, prioridad):
    heap.vector.append([prioridad, dato])
    heap.tamanio += 1
    flotar(heap, heap.tamanio - 1)


def atencion_h(heap):
    primero = heap.vector[0]
    ultimo = heap.vector.pop()
    heap.tamanio -= 1
    if heap.tamanio > 0:
        heap.vector[0] = ultimo
        hundir(heap, 0)
    return primero


class nodoArista(object):
    def __init__(self, info, destino):
        self.info = info
        self.destino = destino
        self.sig = None


class Arista(object):
    def __init__(self):
        self.inicio = None
        self.tamanio = 0


class nodoVertice(object):
    def __init__(self, info):
        self.info = info
        self.sig = None
        self.visitado = False
        self.adyacentes = Arista()


class Grafo(object):
    def __init__(self, dirigido=True):
        self.inicio = None
        self.dirigido = dirigido
        self.tamanio = 0


def insertar_vertice(grafo, dato):
    nodo = nodoVertice(dato)
    if grafo.inicio is None or grafo.inicio.info > dato:
        nodo.sig = grafo.inicio
        grafo.inicio = nodo
    else:
        ant = grafo.inicio
        act = grafo.inicio.sig
        while act is not None and act.info < nodo.info:
            ant = act
            act = act.sig
        nodo.sig = act
        ant.sig = nodo
    grafo.tamanio += 1


def agregar_arista(origen, dato, destino):
    nodo = nodoArista(dato, destino)
    if origen.inicio is None or origen.inicio.destino > destino:
        nodo.sig = origen.inicio
        origen.inicio = nodo
    else:
        ant = origen.inicio
        act = origen.inicio.sig
        while act is not None and act.destino < nodo.destino:
            ant = act
            act = act.sig
        nodo.sig = act
        ant.sig = nodo
    origen.tamanio += 1


def insertar_arista(grafo, dato, origen, destino):
    agregar_arista(origen.adyacentes, dato, destino.info)
    if not grafo.dirigido:
        agregar_arista(destino.adyacentes, dato, origen.info)


def buscar_vertice(grafo, clave):
    aux = grafo.inicio
    while aux is not None and aux.info != clave:
        aux = aux.sig
    return aux


def marcar_no_visitado(grafo):
    aux = grafo.inicio
    while aux is not None:
        aux.visitado = False
        aux = aux.sig


def prim(grafo, origen):
    marcar_no_visitado(grafo)
    inicio = buscar_vertice(grafo, origen)
    inicio.visitado = True
    candidatas = Heap()
    arbol = []
    total = 0
    arista = inicio.adyacentes.inicio
    while arista is not None:
        arribo_h(candidatas, (origen, arista.destino), arista.info)
        arista = arista.sig
    while not heap_vacio(candidatas):
        peso, (desde, hasta) = atencion_h(candidatas)
        vertice = buscar_vertice(grafo, hasta)
        if not vertice.visitado:
            vertice.visitado = True
            arbol.append((desde, hasta, peso))
            total += peso
            arista = vertice.adyacentes.inicio
            while arista is not None:
                if not buscar_vertice(grafo, arista.destino).visitado:
                    arribo_h(candidatas, (hasta, arista.destino), arista.info)
                arista = arista.sig
    return arbol, total


def dijkstra(grafo, origen, destino):
    distancias = {}
    anterior = {}
    aux = grafo.inicio
    while aux is not None:
        distancias[aux.info] = math.inf
        anterior[aux.info] = None
        aux = aux.sig
    distancias[origen] = 0
    pendientes = Heap()
    arribo_h(pendientes, origen, 0)
    while not heap_vacio(pendientes):
        distancia, actual = atencion_h(pendientes)
        if distancia > distancias[actual]:
            continue
        if actual == destino:
            break
        arista = buscar_vertice(grafo, actual).adyacentes.inicio
        while arista is not None:
            nueva = distancia + arista.info
            if nueva < distancias[arista.destino]:
                distancias[arista.destino] = nueva
                anterior[arista.destino] = actual
                arribo_h(pendientes, arista.destino, nueva)
            arista = arista.sig
    camino = []
    actual = destino
    while actual is not None:
        camino.insert(0, actual)
        actual = anterior[actual]
    return camino, distancias[destino]


PERSONAJES = {
    "Luke Skywalker": [4, 5, 6, 7, 8, 9],
    "Darth Vader": [3, 4, 5, 6],
    "Yoda": [1, 2, 3, 5, 6, 8, 9],
    "Boba Fett": [2, 3, 5, 6],
    "C-3PO": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "Leia": [3, 4, 5, 6, 7, 8, 9],
    "Rey": [7, 8, 9],
    "Kylo Ren": [7, 8, 9],
    "Chewbacca": [3, 4, 5, 6, 7, 8, 9],
    "Han Solo": [4, 5, 6, 7, 9],
    "R2-D2": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "BB-8": [7, 8, 9],
}


def cargar_grafo():
    grafo = Grafo(dirigido=False)
    for nombre in PERSONAJES:
        insertar_vertice(grafo, nombre)
    nombres = list(PERSONAJES)
    for i, a in enumerate(nombres):
        for b in nombres[i + 1:]:
            en_comun = len(set(PERSONAJES[a]) & set(PERSONAJES[b]))
            if en_comun > 0:
                insertar_arista(grafo, en_comun, buscar_vertice(grafo, a), buscar_vertice(grafo, b))
    return grafo


def aristas_del_grafo(grafo):
    resultado = []
    vertice = grafo.inicio
    while vertice is not None:
        arista = vertice.adyacentes.inicio
        while arista is not None:
            if vertice.info < arista.destino:
                resultado.append((vertice.info, arista.destino, arista.info))
            arista = arista.sig
        vertice = vertice.sig
    return resultado


def mostrar_expansion_minima(grafo, origen):
    arbol, total = prim(grafo, origen)
    print(f"Arbol de expansion minima desde {origen} (peso total {total}):")
    for desde, hasta, peso in arbol:
        print(f"  {desde} - {hasta} ({peso})")
    print()


def maximo_episodios_compartidos(grafo):
    aristas = aristas_del_grafo(grafo)
    maximo = max(peso for _, _, peso in aristas)
    print(f"Maximo de episodios compartidos: {maximo}")
    for a, b, peso in aristas:
        if peso == maximo:
            print(f"  {a} y {b}")
    print()


def mostrar_camino(grafo, origen, destino):
    camino, costo = dijkstra(grafo, origen, destino)
    print(f"Camino mas corto de {origen} a {destino} (costo {costo}):")
    print("  " + " -> ".join(camino))
    print()


def personajes_en_todos_los_episodios():
    print("Personajes que aparecieron en los nueve episodios:")
    for nombre, episodios in PERSONAJES.items():
        if len(set(episodios)) == 9:
            print(f"  {nombre}")
    print()


def ejercicio_2():
    print()
    print("=" * 60)
    print("EJERCICIO 2 - STAR WARS")
    print("=" * 60)
    grafo = cargar_grafo()

    print("\nAristas del grafo:")
    for a, b, peso in aristas_del_grafo(grafo):
        print(f"  {a} - {b}: {peso}")
    print()

    for origen in ["C-3PO", "Yoda", "Leia"]:
        mostrar_expansion_minima(grafo, origen)

    maximo_episodios_compartidos(grafo)

    mostrar_camino(grafo, "C-3PO", "R2-D2")
    mostrar_camino(grafo, "Yoda", "Darth Vader")

    personajes_en_todos_los_episodios()


if __name__ == "__main__":
    ejercicio_2()
