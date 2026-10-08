import os
import pickle
 
 
class Archivo:
    def __init__(self, ruta):
        self.f = open(ruta, "w+b")
        self.tam = len(self.empaquetar(True, "", 0, 0))
 
    def empaquetar(self, activo, nombre, altura, peso):
        return pickle.dumps((activo, nombre[:40].ljust(40), float(altura), float(peso)))
 
    def cerrar(self):
        self.f.close()
 
    def cantidad(self):
        self.f.seek(0, os.SEEK_END)
        return self.f.tell() // self.tam
 
    def leer(self, nrr):
        self.f.seek(nrr * self.tam)
        activo, nombre, altura, peso = pickle.loads(self.f.read(self.tam))
        return activo, nombre.rstrip(), altura, peso
 
    def escribir(self, nrr, activo, nombre, altura, peso):
        self.f.seek(nrr * self.tam)
        self.f.write(self.empaquetar(activo, nombre, altura, peso))
 
    def agregar(self, nombre, altura, peso):
        nrr = self.cantidad()
        self.escribir(nrr, True, nombre, altura, peso)
        return nrr
 
 
class Nodo:
    def __init__(self, nombre, nrr):
        self.nombre = nombre
        self.nrr = nrr
        self.izq = None
        self.der = None
 
 
class Arbol:
    def __init__(self):
        self.raiz = None
 
    def insertar(self, nombre, nrr):
        self.raiz = self._insertar(self.raiz, nombre, nrr)
 
    def _insertar(self, nodo, nombre, nrr):
        if nodo is None:
            return Nodo(nombre, nrr)
        if nombre < nodo.nombre:
            nodo.izq = self._insertar(nodo.izq, nombre, nrr)
        elif nombre > nodo.nombre:
            nodo.der = self._insertar(nodo.der, nombre, nrr)
        return nodo
 
    def buscar(self, nombre):
        nodo = self.raiz
        while nodo is not None and nodo.nombre != nombre:
            nodo = nodo.izq if nombre < nodo.nombre else nodo.der
        return None if nodo is None else nodo.nrr
 
    def eliminar(self, nombre):
        self.raiz = self._eliminar(self.raiz, nombre)
 
    def _eliminar(self, nodo, nombre):
        if nodo is None:
            return None
        if nombre < nodo.nombre:
            nodo.izq = self._eliminar(nodo.izq, nombre)
        elif nombre > nodo.nombre:
            nodo.der = self._eliminar(nodo.der, nombre)
        elif nodo.izq is None:
            return nodo.der
        elif nodo.der is None:
            return nodo.izq
        else:
            menor = nodo.der
            while menor.izq is not None:
                menor = menor.izq
            nodo.nombre, nodo.nrr = menor.nombre, menor.nrr
            nodo.der = self._eliminar(nodo.der, menor.nombre)
        return nodo
 
    def inorden(self):
        pila, nodo = [], self.raiz
        while pila or nodo:
            while nodo:
                pila.append(nodo)
                nodo = nodo.izq
            nodo = pila.pop()
            yield nodo.nrr
            nodo = nodo.der
 
 
def alta(archivo, arbol, nombre, altura, peso):
    if arbol.buscar(nombre) is not None:
        print("Ya existe", nombre)
        return
    arbol.insertar(nombre, archivo.agregar(nombre, altura, peso))
 
 
def modificar(archivo, arbol, nombre, nuevo_nombre=None, altura=None, peso=None):
    nrr = arbol.buscar(nombre)
    if nrr is None:
        print("No existe", nombre)
        return
    _, _, alt, pes = archivo.leer(nrr)
    nuevo_nombre = nuevo_nombre or nombre
    archivo.escribir(nrr, True, nuevo_nombre,
                     alt if altura is None else altura,
                     pes if peso is None else peso)
    if nuevo_nombre != nombre:
        arbol.eliminar(nombre)
        arbol.insertar(nuevo_nombre, nrr)
 
 
def baja(archivo, arbol, nombre):
    nrr = arbol.buscar(nombre)
    if nrr is None:
        print("No existe", nombre)
        return
    _, nom, alt, pes = archivo.leer(nrr)
    archivo.escribir(nrr, False, nom, alt, pes)
    arbol.eliminar(nombre)
 
 
def mostrar(archivo, nrr):
    _, nombre, altura, peso = archivo.leer(nrr)
    print(f"{nombre:<18} {altura:.2f} m  {peso:.1f} kg")
 
 
def mostrar_personajes(archivo, arbol, nombres):
    for nombre in nombres:
        nrr = arbol.buscar(nombre)
        if nrr is None:
            print(nombre, "no esta en el archivo")
        else:
            mostrar(archivo, nrr)
 
 
def listar_mas_de_1_metro(archivo, arbol):
    for nrr in arbol.inorden():
        if archivo.leer(nrr)[2] > 1:
            mostrar(archivo, nrr)
 
 
def listar_menos_de_75_kilos(archivo, arbol):
    for nrr in arbol.inorden():
        if archivo.leer(nrr)[3] < 75:
            mostrar(archivo, nrr)
 
 
DATOS = [
    ("Yoda", 0.66, 17), ("Boba Fett", 1.83, 78.2), ("Luke Skywalker", 1.72, 77),
    ("Darth Vader", 2.02, 136), ("R2-D2", 0.96, 32), ("C-3PO", 1.67, 75),
    ("Chewbacca", 2.28, 112), ("Leia Organa", 1.50, 49), ("Han Solo", 1.80, 80),
]
 
if __name__ == "__main__":
    archivo = Archivo("personajes.dat")
    arbol = Arbol()
    for nombre, altura, peso in DATOS:
        alta(archivo, arbol, nombre, altura, peso)
 
    print("--- Yoda y Boba Fett ---")
    mostrar_personajes(archivo, arbol, ["Yoda", "Boba Fett"])
 
    print("\n--- Miden mas de 1 metro ---")
    listar_mas_de_1_metro(archivo, arbol)
 
    print("\n--- Pesan menos de 75 kilos ---")
    listar_menos_de_75_kilos(archivo, arbol)
 
    print("\n--- Alta de Mace Windu, modificacion de Yoda y baja de Han Solo ---")
    alta(archivo, arbol, "Mace Windu", 1.88, 84)
    modificar(archivo, arbol, "Yoda", peso=18)
    baja(archivo, arbol, "Han Solo")
    for nrr in arbol.inorden():
        mostrar(archivo, nrr)
 
    archivo.cerrar()
