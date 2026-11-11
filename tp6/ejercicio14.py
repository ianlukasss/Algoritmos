from grafo import Grafo

casa = Grafo()
ambientes = ["cocina", "comedor", "cochera", "quincho", "baño 1", "baño 2",
             "habitación 1", "habitación 2", "sala de estar", "terraza", "patio"]
for a in ambientes:
    casa.agregar_nodo(a)

# (ambiente, ambiente, distancia en metros)
aristas = [
    ("cocina", "comedor", 4), ("cocina", "patio", 5), ("cocina", "quincho", 7),
    ("cocina", "cochera", 8),
    ("comedor", "sala de estar", 3), ("comedor", "patio", 6), ("comedor", "baño 1", 5),
    ("cochera", "patio", 4), ("cochera", "quincho", 6),
    ("quincho", "patio", 3), ("quincho", "terraza", 7), ("quincho", "baño 2", 5),
    ("baño 1", "habitación 1", 3), ("baño 1", "sala de estar", 4), ("baño 1", "habitación 2", 4),
    ("baño 2", "patio", 5), ("baño 2", "terraza", 4),
    ("habitación 1", "habitación 2", 4), ("habitación 1", "sala de estar", 6),
    ("habitación 1", "terraza", 9),
    ("habitación 2", "sala de estar", 5), ("habitación 2", "terraza", 6),
]
for a, b, m in aristas:
    casa.agregar_arista(a, b, m)

# Verificación de la consigna (b): >= 3 aristas por vértice y exactamente dos con 5
grados = {v: len(casa.ady[v]) for v in casa.ady}
assert all(g >= 3 for g in grados.values())
assert sum(1 for g in grados.values() if g == 5) == 2
print("Grados:", grados, "\n")

# (c) Árbol de expansión mínima
arbol, total = casa.arbol_expansion_minima()
print("Árbol de expansión mínima:")
for a, b, m in arbol:
    print(f"  {a} - {b}: {m} m")
print(f"Cable total necesario: {total} m\n")

# (d) Camino más corto habitación 1 -> sala de estar
camino, metros = casa.camino_mas_corto("habitación 1", "sala de estar")
print("Camino router -> Smart TV:", " -> ".join(camino))
print(f"Cable de red necesario: {metros} m")
