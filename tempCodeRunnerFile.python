# Punto 24, torre de Hanói.
def hanoi(n, origen, auxiliar, destino):

    
    if n == 1:
        print(f"Mover disco 1 desde {origen} hasta {destino}")
        return

    
    hanoi(n - 1, origen, destino, auxiliar)

  
    print(f"Mover disco {n} desde {origen} hasta {destino}")


    hanoi(n - 1, auxiliar, origen, destino)


discos = int(input("Ingrese la cantidad de discos: "))

hanoi(discos, "Aguja 1", "Aguja 2", "Aguja 3")