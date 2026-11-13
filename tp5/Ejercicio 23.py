import unicodedata
from collections import Counter, deque


def clave(texto):
    base = unicodedata.normalize("NFD", texto)
    return "".join(c for c in base if unicodedata.category(c) != "Mn").lower()


class NodoCriatura:
    def __init__(self, nombre, derrotado_por=None):
        self.nombre = nombre
        self.derrotado_por = derrotado_por
        self.descripcion = ""
        self.capturada = None
        self.izq = None
        self.der = None

    def mostrar(self):
        derrotado = self.derrotado_por if self.derrotado_por else "nadie"
        capturada = self.capturada if self.capturada else "nadie"
        descripcion = self.descripcion if self.descripcion else "sin descripción"
        print(f"  Criatura: {self.nombre}")
        print(f"  Derrotada por: {derrotado}")
        print(f"  Capturada por: {capturada}")
        print(f"  Descripción: {descripcion}")


class ArbolCriaturas:
    def __init__(self):
        self.raiz = None

    def insertar(self, nodo):
        if self.raiz is None:
            self.raiz = nodo
            return
        actual = self.raiz
        while True:
            if clave(nodo.nombre) < clave(actual.nombre):
                if actual.izq is None:
                    actual.izq = nodo
                    return
                actual = actual.izq
            else:
                if actual.der is None:
                    actual.der = nodo
                    return
                actual = actual.der

    def inorden(self, nodo=None, primero=True):
        if primero:
            nodo = self.raiz
        if nodo is not None:
            yield from self.inorden(nodo.izq, False)
            yield nodo
            yield from self.inorden(nodo.der, False)

    def por_nivel(self):
        if self.raiz is None:
            return
        cola = deque([(self.raiz, 0)])
        while cola:
            nodo, nivel = cola.popleft()
            yield nodo, nivel
            if nodo.izq:
                cola.append((nodo.izq, nivel + 1))
            if nodo.der:
                cola.append((nodo.der, nivel + 1))

    def buscar(self, nombre):
        actual = self.raiz
        while actual is not None:
            if clave(nombre) == clave(actual.nombre):
                return actual
            actual = actual.izq if clave(nombre) < clave(actual.nombre) else actual.der
        return None

    def buscar_coincidencia(self, texto):
        return [n for n in self.inorden() if clave(texto) in clave(n.nombre)]

    def eliminar(self, nombre):
        self.raiz, eliminado = self._eliminar(self.raiz, nombre)
        return eliminado

    def _eliminar(self, nodo, nombre):
        if nodo is None:
            return None, None
        eliminado = None
        if clave(nombre) < clave(nodo.nombre):
            nodo.izq, eliminado = self._eliminar(nodo.izq, nombre)
        elif clave(nombre) > clave(nodo.nombre):
            nodo.der, eliminado = self._eliminar(nodo.der, nombre)
        else:
            eliminado = nodo
            if nodo.izq is None:
                return nodo.der, eliminado
            if nodo.der is None:
                return nodo.izq, eliminado
            sucesor = nodo.der
            while sucesor.izq is not None:
                sucesor = sucesor.izq
            datos = (sucesor.nombre, sucesor.derrotado_por,
                     sucesor.descripcion, sucesor.capturada)
            nodo.der, _ = self._eliminar(nodo.der, sucesor.nombre)
            copia = NodoCriatura(eliminado.nombre, eliminado.derrotado_por)
            copia.descripcion = eliminado.descripcion
            copia.capturada = eliminado.capturada
            eliminado = copia
            nodo.nombre, nodo.derrotado_por, nodo.descripcion, nodo.capturada = datos
        return nodo, eliminado

    def cargar_descripcion(self, nombre, texto):
        nodo = self.buscar(nombre)
        if nodo is not None:
            nodo.descripcion = texto
            return True
        return False

    def renombrar(self, nombre_viejo, nombre_nuevo):
        nodo = self.eliminar(nombre_viejo)
        if nodo is None:
            return False
        nodo.nombre = nombre_nuevo
        nodo.izq = None
        nodo.der = None
        self.insertar(nodo)
        return True


tabla = [
    ("Ceto", None), ("Tifón", "Zeus"), ("Equidna", "Argos Panoptes"),
    ("Dino", None), ("Pefredo", None), ("Enio", None), ("Escila", None),
    ("Caribdis", None), ("Euríale", None), ("Esteno", None),
    ("Medusa", "Perseo"), ("Ladón", "Heracles"), ("Águila del Cáucaso", None),
    ("Quimera", "Belerofonte"), ("Hidra de Lerna", "Heracles"),
    ("León de Nemea", "Heracles"), ("Esfinge", "Edipo"),
    ("Dragón de la Cólquida", None), ("Cerbero", None),
    ("Cerda de Cromión", "Teseo"), ("Ortro", "Heracles"),
    ("Toro de Creta", "Teseo"), ("Jabalí de Calidón", "Atalanta"),
    ("Carcinos", None), ("Gerión", "Heracles"), ("Cloto", None),
    ("Láquesis", None), ("Átropos", None), ("Minotauro de Creta", "Teseo"),
    ("Harpías", None), ("Argos Panoptes", "Hermes"),
    ("Aves del Estínfalo", None), ("Talos", "Medea"), ("Sirenas", None),
    ("Pitón", "Apolo"), ("Cierva de Cerinea", None), ("Basilisco", None),
    ("Jabalí de Erimanto", None),
]

arbol = ArbolCriaturas()
for nombre, vencedor in tabla:
    arbol.insertar(NodoCriatura(nombre, vencedor))

arbol.cargar_descripcion("Talos", "Gigante de bronce que protegía la isla de Creta.")
arbol.cargar_descripcion("Cerbero", "Perro de tres cabezas guardián del Hades.")
arbol.cargar_descripcion("Hidra de Lerna", "Serpiente acuática de múltiples cabezas que se regeneraban.")
arbol.cargar_descripcion("Quimera", "Monstruo con cabeza de león, cuerpo de cabra y cola de serpiente.")
arbol.cargar_descripcion("Medusa", "Gorgona cuya mirada convertía en piedra.")
arbol.cargar_descripcion("Minotauro de Creta", "Mitad hombre, mitad toro, encerrado en el laberinto.")
arbol.cargar_descripcion("Esfinge", "Criatura alada que planteaba un enigma a los viajeros.")

print("a. Listado inorden de criaturas y quiénes las derrotaron:")
for n in arbol.inorden():
    print(f"   {n.nombre} - {n.derrotado_por if n.derrotado_por else 'sin derrotar'}")

print("\nc. Información de Talos:")
arbol.buscar("Talos").mostrar()

print("\nd. Los 3 héroes o dioses que derrotaron más criaturas:")
conteo = Counter(n.derrotado_por for n in arbol.inorden() if n.derrotado_por)
for heroe, cantidad in conteo.most_common(3):
    print(f"   {heroe}: {cantidad}")

print("\ne. Criaturas derrotadas por Heracles:")
for n in arbol.inorden():
    if n.derrotado_por == "Heracles":
        print("  ", n.nombre)

print("\nf. Criaturas que no han sido derrotadas:")
for n in arbol.inorden():
    if n.derrotado_por is None:
        print("  ", n.nombre)

print("\nh. Heracles atrapó a Cerbero, Toro de Creta, Cierva Cerinea y Jabalí de Erimanto:")
for texto in ["Cerbero", "Toro de Creta", "Cierva", "Jabalí de Erimanto"]:
    for n in arbol.buscar_coincidencia(texto):
        n.capturada = "Heracles"
        print("   Modificada:", n.nombre)

print("\ni. Búsqueda por coincidencia de 'Jabal':")
for n in arbol.buscar_coincidencia("Jabal"):
    print("  ", n.nombre)

print("\nj. Eliminación de Basilisco y Sirenas:")
for nombre in ["Basilisco", "Sirenas"]:
    eliminado = arbol.eliminar(nombre)
    print("   Eliminada:" if eliminado else "   No encontrada:", nombre)

print("\nk. Aves del Estínfalo: Heracles derrotó a varias")
aves = arbol.buscar("Aves del Estínfalo")
aves.derrotado_por = "Heracles"
aves.descripcion = "Aves de plumas metálicas; Heracles derrotó a varias."
aves.mostrar()

print("\nl. Ladón pasa a llamarse Dragón Ladón:")
if arbol.renombrar("Ladón", "Dragón Ladón"):
    arbol.buscar("Dragón Ladón").mostrar()

print("\nm. Listado por nivel:")
nivel_actual = -1
for n, nivel in arbol.por_nivel():
    if nivel != nivel_actual:
        nivel_actual = nivel
        print(f"   Nivel {nivel}:")
    print("      ", n.nombre)

print("\nn. Criaturas capturadas por Heracles:")
for n in arbol.inorden():
    if n.capturada == "Heracles":
        print("  ", n.nombre)