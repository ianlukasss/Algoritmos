import json
import os
from collections import deque
 
RUTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jedis.json")
 
# Datos de ejemplo: se crean solo si el archivo no existe
DATOS_EJEMPLO = [
    {"nombre": "Yoda", "especie": "Desconocida", "anio_nacimiento": -896,
     "sable": ["Verde"], "ranking": ["Jedi Master"], "maestros": []},
    {"nombre": "Luke Skywalker", "especie": "Humano", "anio_nacimiento": -19,
     "sable": ["Verde", "Azul"], "ranking": ["Padawan", "Jedi Knight", "Jedi Master"],
     "maestros": ["Obi-Wan Kenobi", "Yoda"]},
    {"nombre": "Obi-Wan Kenobi", "especie": "Humano", "anio_nacimiento": -57,
     "sable": ["Azul"], "ranking": ["Padawan", "Jedi Knight", "Jedi Master"],
     "maestros": ["Qui-Gon Jinn", "Yoda"]},
    {"nombre": "Qui-Gon Jinn", "especie": "Humano", "anio_nacimiento": -92,
     "sable": ["Verde"], "ranking": ["Padawan", "Jedi Knight", "Jedi Master"],
     "maestros": ["Dooku"]},
    {"nombre": "Ahsoka Tano", "especie": "Togruta", "anio_nacimiento": -36,
     "sable": ["Verde", "Azul", "Blanco"], "ranking": ["Padawan"],
     "maestros": ["Anakin Skywalker"]},
    {"nombre": "Anakin Skywalker", "especie": "Humano", "anio_nacimiento": -41,
     "sable": ["Azul"], "ranking": ["Padawan", "Jedi Knight"],
     "maestros": ["Obi-Wan Kenobi"]},
    {"nombre": "Plo Koon", "especie": "Kel Dor", "anio_nacimiento": -382,
     "sable": ["Azul"], "ranking": ["Jedi Master"], "maestros": ["Yoda"]},
    {"nombre": "Shaak Ti", "especie": "Togruta", "anio_nacimiento": -52,
     "sable": ["Azul"], "ranking": ["Jedi Master"], "maestros": []},
    {"nombre": "Ki-Adi-Mundi", "especie": "Cerean", "anio_nacimiento": -92,
     "sable": ["Azul"], "ranking": ["Jedi Master"], "maestros": []},
    {"nombre": "Aayla Secura", "especie": "Twi'lek", "anio_nacimiento": -48,
     "sable": ["Azul"], "ranking": ["Jedi Knight"], "maestros": ["Quinlan Vos"]},
]
 
 
# ---------- Árbol binario de búsqueda ----------
class Nodo:
    def __init__(self, clave, dato):
        self.clave = clave
        self.datos = [dato]      # lista: permite claves repetidas (ranking, especie)
        self.izq = None
        self.der = None
 
 
class Arbol:
    def __init__(self):
        self.raiz = None
 
    def insertar(self, clave, dato):
        self.raiz = self._insertar(self.raiz, clave, dato)
 
    def _insertar(self, nodo, clave, dato):
        if nodo is None:
            return Nodo(clave, dato)
        if clave < nodo.clave:
            nodo.izq = self._insertar(nodo.izq, clave, dato)
        elif clave > nodo.clave:
            nodo.der = self._insertar(nodo.der, clave, dato)
        else:
            nodo.datos.append(dato)
        return nodo
 
    def buscar(self, clave):
        nodo = self.raiz
        while nodo:
            if clave == nodo.clave:
                return nodo.datos
            nodo = nodo.izq if clave < nodo.clave else nodo.der
        return []
 
    def inorden(self):
        def _in(nodo):
            if nodo:
                yield from _in(nodo.izq)
                for d in nodo.datos:
                    yield nodo.clave, d
                yield from _in(nodo.der)
        return _in(self.raiz)
 
    def por_nivel(self):
        if self.raiz is None:
            return
        cola = deque([self.raiz])
        while cola:
            nodo = cola.popleft()
            for d in nodo.datos:
                yield nodo.clave, d
            if nodo.izq:
                cola.append(nodo.izq)
            if nodo.der:
                cola.append(nodo.der)
 
 
# ---------- Utilidades ----------
def cargar_jedis(ruta):
    if not os.path.exists(ruta):
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(DATOS_EJEMPLO, f, ensure_ascii=False, indent=2)
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)
 
 
def mostrar_jedi(j):
    print(f"Nombre: {j['nombre']}")
    print(f"  Especie: {j['especie']}")
    print(f"  Año de nacimiento: {j['anio_nacimiento']}")
    print(f"  Sable de luz: {', '.join(j['sable'])}")
    print(f"  Ranking: {', '.join(j['ranking'])}")
    print(f"  Maestros: {', '.join(j['maestros']) if j['maestros'] else '-'}")
 
 
# a. crear los tres árboles
def crear_arboles(jedis):
    por_nombre, por_ranking, por_especie = Arbol(), Arbol(), Arbol()
    for j in jedis:
        por_nombre.insertar(j["nombre"], j)
        for r in j["ranking"]:
            por_ranking.insertar(r, j)
        por_especie.insertar(j["especie"], j)
    return por_nombre, por_ranking, por_especie
 
 
# b. barrido inorden por nombre y por ranking
def barrido_inorden(arbol_nombre, arbol_ranking):
    print("--- Inorden por nombre ---")
    for clave, _ in arbol_nombre.inorden():
        print(clave)
    print("--- Inorden por ranking ---")
    for clave, j in arbol_ranking.inorden():
        print(f"{clave}: {j['nombre']}")
 
 
# c. barrido por nivel por ranking y por especie
def barrido_por_nivel(arbol_ranking, arbol_especie):
    print("--- Por nivel (ranking) ---")
    for clave, j in arbol_ranking.por_nivel():
        print(f"{clave}: {j['nombre']}")
    print("--- Por nivel (especie) ---")
    for clave, j in arbol_especie.por_nivel():
        print(f"{clave}: {j['nombre']}")
 
 
# d. toda la información de Yoda y Luke Skywalker
def mostrar_yoda_luke(arbol_nombre):
    for nombre in ("Yoda", "Luke Skywalker"):
        encontrados = arbol_nombre.buscar(nombre)
        if encontrados:
            for j in encontrados:
                mostrar_jedi(j)
        else:
            print(f"{nombre} no está en el archivo")
 
 
# e. todos los Jedi Master
def mostrar_masters(arbol_ranking):
    for j in arbol_ranking.buscar("Jedi Master"):
        print(j["nombre"])
 
 
# f. Jedi que usaron sable verde
def sable_verde(arbol_nombre):
    for _, j in arbol_nombre.inorden():
        if "Verde" in j["sable"]:
            print(j["nombre"])
 
 
# g. Jedi cuyos maestros están en el archivo
def maestros_en_archivo(arbol_nombre):
    for _, j in arbol_nombre.inorden():
        presentes = [m for m in j["maestros"] if arbol_nombre.buscar(m)]
        if presentes:
            print(f"{j['nombre']} -> maestros en archivo: {', '.join(presentes)}")
 
 
# h. especie Togruta o Cerean
def togruta_o_cerean(arbol_especie):
    for esp in ("Togruta", "Cerean"):
        for j in arbol_especie.buscar(esp):
            print(f"{j['nombre']} ({esp})")
 
 
# i. nombres que comienzan con A y nombres que contienen "-"
def filtrar_nombres(arbol_nombre):
    print("--- Comienzan con A ---")
    for nombre, _ in arbol_nombre.inorden():
        if nombre.startswith("A"):
            print(nombre)
    print("--- Contienen '-' ---")
    for nombre, _ in arbol_nombre.inorden():
        if "-" in nombre:
            print(nombre)
 
 
# ---------- Programa principal ----------
if __name__ == "__main__":
    jedis = cargar_jedis(RUTA)
    a_nombre, a_ranking, a_especie = crear_arboles(jedis)              # a
 
    barrido_inorden(a_nombre, a_ranking)                               # b
    barrido_por_nivel(a_ranking, a_especie)                            # c
    print("--- Yoda y Luke ---");   mostrar_yoda_luke(a_nombre)        # d
    print("--- Jedi Master ---");   mostrar_masters(a_ranking)         # e
    print("--- Sable verde ---");   sable_verde(a_nombre)              # f
    print("--- Maestros en archivo ---"); maestros_en_archivo(a_nombre)  # g
    print("--- Togruta / Cerean ---"); togruta_o_cerean(a_especie)     # h
    filtrar_nombres(a_nombre)          
