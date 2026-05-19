# Punto 20.

def busquedaSecuencial(lista, valor, i=0):

    # Caso base: se encontró el valor
    if lista[i] == valor:
        return i

    # Llamada recursiva
    return busquedaSecuencial(lista, valor, i + 1)


lista = []

n = int(input("Ingrese la cantidad de elementos: "))

for i in range(n):
    num = int(input("Ingrese un número: "))
    lista.append(num)

valor = int(input("Ingrese el valor a buscar: "))

lista.append(valor)

posicion = busquedaSecuencial(lista, valor)

if posicion < n:
    print("El valor SI se encuentra en la lista.")
    print("Posición:", posicion)
else:
    print("El valor NO se encuentra en la lista.")

lista.pop()