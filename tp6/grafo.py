import heapq
from collections import deque


class Grafo:
    def __init__(self):
        self.tipos = {} 
        self.ady = {}    

    def agregar_nodo(self, nombre, tipo=None):
        self.tipos[nombre] = tipo
        self.ady.setdefault(nombre, {})

    def agregar_arista(self, a, b, peso=1):
        if a not in self.ady or b not in self.ady:
            raise ValueError(f"Nodo inexistente en la arista {a} - {b}")
        self.ady[a][b] = peso
        self.ady[b][a] = peso

    def aristas(self):
        vistas, res = set(), []
        for a in self.ady:
            for b, p in self.ady[a].items():
                if (b, a) not in vistas:
                    vistas.add((a, b))
                    res.append((a, b, p))
        return res

   
    def profundidad(self, inicio):
        visitados, orden, pila = set(), [], [inicio]
        while pila:
            v = pila.pop()
            if v in visitados:
                continue
            visitados.add(v)
            orden.append(v)
            for w in reversed(list(self.ady[v])):
                if w not in visitados:
                    pila.append(w)
        return orden

    def amplitud(self, inicio):
        visitados, orden, cola = {inicio}, [], deque([inicio])
        while cola:
            v = cola.popleft()
            orden.append(v)
            for w in self.ady[v]:
                if w not in visitados:
                    visitados.add(w)
                    cola.append(w)
        return orden
    
    def dijkstra(self, origen):
        dist = {v: float("inf") for v in self.ady}
        prev = {v: None for v in self.ady}
        dist[origen] = 0
        heap = [(0, origen)]
        while heap:
            d, v = heapq.heappop(heap)
            if d > dist[v]:
                continue
            for w, p in self.ady[v].items():
                if d + p < dist[w]:
                    dist[w] = d + p
                    prev[w] = v
                    heapq.heappush(heap, (dist[w], w))
        return dist, prev

    def camino_mas_corto(self, origen, destino):
        dist, prev = self.dijkstra(origen)
        if dist[destino] == float("inf"):
            return None, float("inf")
        camino, v = [], destino
        while v is not None:
            camino.append(v)
            v = prev[v]
        return camino[::-1], dist[destino]

    def arbol_expansion_minima(self):
        padre = {v: v for v in self.ady}

        def buscar(x):
            while padre[x] != x:
                padre[x] = padre[padre[x]]
                x = padre[x]
            return x

        arbol, total = [], 0
        for a, b, p in sorted(self.aristas(), key=lambda e: e[2]):
            ra, rb = buscar(a), buscar(b)
            if ra != rb:
                padre[ra] = rb
                arbol.append((a, b, p))
                total += p
        return arbol, total
