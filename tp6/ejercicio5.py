from grafo import Grafo


NODOS = [
    ("Manjaro", "pc"), ("Fedora", "pc"), ("Red Hat PC", "pc"), ("Ubuntu", "pc"), ("Mint", "pc"),
    ("Red Hat", "notebook"), ("Debian", "notebook"), ("Arch", "notebook"),
    ("Guaraní", "servidor"), ("MongoDB", "servidor"),
    ("Router 1", "router"), ("Router 2", "router"),
    ("Switch 01", "switch"), ("Switch 02", "switch"), ("Switch 03", "switch"),
    ("Impresora", "impresora"),
]
ARISTAS = [
    ("Switch 01", "Manjaro", 1), ("Switch 01", "Red Hat", 1), ("Switch 01", "Debian", 1),
    ("Switch 01", "Router 1", 3),
    ("Switch 02", "Fedora", 1), ("Switch 02", "Red Hat PC", 1), ("Switch 02", "Arch", 1), ("Switch 02", "Impresora", 2),
    ("Switch 02", "Router 1", 4), ("Switch 02", "Router 2", 5),
    ("Switch 03", "Ubuntu", 1), ("Switch 03", "Mint", 1), ("Switch 03", "Guaraní", 2),
    ("Switch 03", "MongoDB", 3), ("Switch 03", "Router 2", 2),
    ("Router 1", "Router 2", 6),
]

red = Grafo()
for nombre, tipo in NODOS:
    red.agregar_nodo(nombre, tipo)
for a, b, p in ARISTAS:
    red.agregar_arista(a, b, p)

print("== (b) Barridos ==")
for nb in ["Red Hat", "Debian", "Arch"]:
    print(f"Profundidad desde {nb}: {red.profundidad(nb)}")
    print(f"Amplitud    desde {nb}: {red.amplitud(nb)}")

for pc in ["Manjaro", "Red Hat PC", "Fedora"]:
    camino, costo = red.camino_mas_corto(pc, "Impresora")
    print(f"{pc}: {' -> '.join(camino)} (costo {costo})")

print("\n== (d) Árbol de expansión mínima ==")
arbol, total = red.arbol_expansion_minima()
for a, b, p in arbol:
    print(f"  {a} - {b} ({p})")
print("Costo total:", total)


def mejor_origen(candidatos, destino):
    """Devuelve (equipo, camino, costo) del candidato con camino más corto al destino."""
    mejor = None
    for c in candidatos:
        camino, costo = red.camino_mas_corto(c, destino)
        if camino and (mejor is None or costo < mejor[2]):
            mejor = (c, camino, costo)
    return mejor


print("\n== (e) pc más cercana a Guaraní ==")
pcs = [n for n, t in red.tipos.items() if t == "pc"]
eq, camino, costo = mejor_origen(pcs, "Guaraní")
print(f"{eq}: {' -> '.join(camino)} (costo {costo})")

print("\n== (f) Switch 01 -> MongoDB ==")
compus = [v for v in red.ady["Switch 01"] if red.tipos[v] in ("pc", "notebook")]
eq, camino, costo = mejor_origen(compus, "MongoDB")
print(f"{eq}: {' -> '.join(camino)} (costo {costo})")
