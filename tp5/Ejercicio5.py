class NodoArbol:
    def __init__(self, nombre, heroe):
        self.nombre = nombre
        self.heroe = heroe
        self.izq = None
        self.der = None


class Arbol:
    def __init__(self):
        self.raiz = None

    def insertar(self, nombre, heroe):
        nuevo = NodoArbol(nombre, heroe)
        if self.raiz is None:
            self.raiz = nuevo
            return
        actual = self.raiz
        while True:
            if nombre < actual.nombre:
                if actual.izq is None:
                    actual.izq = nuevo
                    return
                actual = actual.izq
            else:
                if actual.der is None:
                    actual.der = nuevo
                    return
                actual = actual.der

    def inorden(self, nodo=None, primero=True):
        if primero:
            nodo = self.raiz
        if nodo is not None:
            yield from self.inorden(nodo.izq, False)
            yield nodo
            yield from self.inorden(nodo.der, False)

    def inorden_desc(self, nodo=None, primero=True):
        if primero:
            nodo = self.raiz
        if nodo is not None:
            yield from self.inorden_desc(nodo.der, False)
            yield nodo
            yield from self.inorden_desc(nodo.izq, False)

    def contar(self):
        return sum(1 for _ in self.inorden())

    def buscar_proximidad(self, clave):
        clave = clave.lower()
        return [n for n in self.inorden() if clave in n.nombre.lower()]

    def eliminar(self, nombre):
        self.raiz, eliminado = self._eliminar(self.raiz, nombre)
        return eliminado

    def _eliminar(self, nodo, nombre):
        if nodo is None:
            return None, None
        eliminado = None
        if nombre < nodo.nombre:
            nodo.izq, eliminado = self._eliminar(nodo.izq, nombre)
        elif nombre > nodo.nombre:
            nodo.der, eliminado = self._eliminar(nodo.der, nombre)
        else:
            eliminado = (nodo.nombre, nodo.heroe)
            if nodo.izq is None:
                return nodo.der, eliminado
            if nodo.der is None:
                return nodo.izq, eliminado
            sucesor = nodo.der
            while sucesor.izq is not None:
                sucesor = sucesor.izq
            nodo.nombre, nodo.heroe = sucesor.nombre, sucesor.heroe
            nodo.der, _ = self._eliminar(nodo.der, sucesor.nombre)
        return nodo, eliminado

    def modificar_nombre(self, nombre_viejo, nombre_nuevo):
        eliminado = self.eliminar(nombre_viejo)
        if eliminado is not None:
            self.insertar(nombre_nuevo, eliminado[1])
            return True
        return False


def generar_bosque(arbol):
    arbol_heroes = Arbol()
    arbol_villanos = Arbol()
    for nodo in arbol.inorden():
        destino = arbol_heroes if nodo.heroe else arbol_villanos
        destino.insertar(nodo.nombre, nodo.heroe)
    return arbol_heroes, arbol_villanos


personajes = [
    ("Iron Man", True),
    ("Captain America", True),
    ("Thor", True),
    ("Hulk", True),
    ("Black Widow", True),
    ("Hawkeye", True),
    ("Black Panther", True),
    ("Spider-Man", True),
    ("Dr Strangee", True),
    ("Captain Marvel", True),
    ("Ant-Man", True),
    ("Scarlet Witch", True),
    ("Vision", True),
    ("Falcon", True),
    ("Winter Soldier", True),
    ("Star-Lord", True),
    ("Gamora", True),
    ("Drax", True),
    ("Rocket Raccoon", True),
    ("Groot", True),
    ("Loki", False),
    ("Thanos", False),
    ("Ultron", False),
    ("Red Skull", False),
    ("Hela", False),
    ("Killmonger", False),
    ("Ronan", False),
    ("Ego", False),
    ("Vulture", False),
    ("Mysterio", False),
    ("Dormammu", False),
    ("Kaecilius", False),
]

personajes_desordenados = [personajes[i] for i in
                           [10, 21, 3, 27, 0, 15, 8, 30, 5, 18, 24, 1, 12,
                            29, 7, 20, 14, 25, 2, 31, 9, 17, 22, 4, 28, 13,
                            19, 6, 26, 11, 23, 16]]

mcu = Arbol()
for nombre, es_heroe in personajes_desordenados:
    mcu.insertar(nombre, es_heroe)

print("b. Villanos ordenados alfabéticamente:")
for n in mcu.inorden():
    if not n.heroe:
        print("  ", n.nombre)

print("\nc. Superhéroes que empiezan con C:")
for n in mcu.inorden():
    if n.heroe and n.nombre.startswith("C"):
        print("  ", n.nombre)

print("\nd. Cantidad de superhéroes:", sum(1 for n in mcu.inorden() if n.heroe))

print("\ne. Búsqueda por proximidad de 'Strange':")
encontrados = mcu.buscar_proximidad("Strange")
for n in encontrados:
    print("   Encontrado:", n.nombre)
if encontrados:
    viejo = encontrados[0].nombre
    mcu.modificar_nombre(viejo, "Doctor Strange")
    print("   Nombre corregido a: Doctor Strange")

print("\nf. Superhéroes en orden descendente:")
for n in mcu.inorden_desc():
    if n.heroe:
        print("  ", n.nombre)

arbol_heroes, arbol_villanos = generar_bosque(mcu)

print("\ng. Bosque")
print("   I. Nodos del árbol de superhéroes:", arbol_heroes.contar())
print("      Nodos del árbol de villanos:", arbol_villanos.contar())

print("   II. Barrido alfabético del árbol de superhéroes:")
for n in arbol_heroes.inorden():
    print("      ", n.nombre)

print("       Barrido alfabético del árbol de villanos:")
for n in arbol_villanos.inorden():
    print("      ", n.nombre)