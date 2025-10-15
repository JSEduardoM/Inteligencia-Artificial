import time
import networkx as nx
import matplotlib.pyplot as plt
import heapq
from collections import deque

class GraphVisualizer:
    def __init__(self):
        self.G = nx.Graph()
        self.pos = {} 

    def add_edge(self, u, v, w=1):
        self.G.add_edge(u, v, weight=w)

    def set_positions(self, pos_dict):
        """Establecer posiciones personalizadas para los nodos"""
        self.pos = pos_dict

    def draw(self, visited=None, path=None, current=None, structure=None, algo_name="Algoritmo"):
        visited = visited or []
        path = path or []

        plt.clf()  

        node_colors = [
            '#FF4444' if n == current else
            '#FFA500' if n in path else
            '#FFFF00' if n in visited else
            '#87CEEB' for n in self.G.nodes()
        ]

        nx.draw_networkx_nodes(self.G, self.pos, node_color=node_colors, node_size=1400)
        nx.draw_networkx_labels(self.G, self.pos, font_size=12, font_weight='bold')
        nx.draw_networkx_edges(self.G, self.pos, width=2, edge_color='gray', alpha=0.6)
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=nx.get_edge_attributes(self.G, 'weight'))

        plt.title(f"{algo_name} - Nodo actual: {current if current else 'Iniciando...'}", fontsize=14, color='green')

        if structure:
            s_display = ', '.join(map(str, structure[:5])) + ('...' if len(structure) > 5 else '')
            plt.xlabel(f"Estructura: [{s_display}]", fontsize=12)

        plt.axis('off')
        plt.tight_layout()
        plt.pause(0.5)  # pausa para animación

# DFS 

def dfs_step_by_step(graph: GraphVisualizer, start: str, delay=1.0):
    visited = []
    stack = [start]

    print("\n" + "="*60)
    print("DFS - Búsqueda en Profundidad")
    print("="*60)
    print(f"Inicializar pila: {stack}, visitados: {visited}\n")

    plt.ion()
    plt.figure(figsize=(10,7))  # figura única

    step = 1
    while stack:
        current = stack.pop()
        print(f"Paso {step}: Sacar de pila: {current}")

        if current not in visited:
            visited.append(current)
            print(f"         Visitar: {current} | Visitados: {visited}")

            neighbors = [n for n in sorted(graph.G.neighbors(current)) if n not in visited]
            stack.extend(sorted(neighbors, reverse=True))
            print(f"         Empujar vecinos: {neighbors} | Pila: {stack}\n")

            graph.draw(visited=visited, current=current, structure=stack, algo_name="DFS")
            time.sleep(delay)
            step += 1

    print(f"DFS COMPLETO! Orden: {' → '.join(visited)}")
    graph.draw(visited=visited, algo_name="DFS COMPLETADO")
    plt.ioff()
    plt.show()

# BFS

def bfs_step_by_step(graph: GraphVisualizer, start: str, delay=1.0):
    visited = []
    queue = deque([start])

    print("\n" + "="*60)
    print("BFS - Búsqueda en Anchura")
    print("="*60)
    print(f"Inicializar cola: {list(queue)}, visitados: {visited}\n")

    plt.ion()
    plt.figure(figsize=(10,7))  # figura única

    step = 1
    while queue:
        current = queue.popleft()
        print(f"Paso {step}: Extraer de cola: {current}")

        if current not in visited:
            visited.append(current)
            print(f"         Visitar: {current} | Visitados: {visited}")

            neighbors = [n for n in sorted(graph.G.neighbors(current)) if n not in visited]
            queue.extend(neighbors)
            print(f"         Encolar vecinos: {neighbors} | Cola: {list(queue)}\n")

            graph.draw(visited=visited, current=current, structure=list(queue), algo_name="BFS")
            time.sleep(delay)
            step += 1

    print(f"BFS COMPLETO! Orden: {' → '.join(visited)}")
    graph.draw(visited=visited, algo_name="BFS COMPLETADO")
    plt.ioff()
    plt.show()

# UCS

def ucs_step_by_step(graph: GraphVisualizer, start: str, goal: str, delay=1.0):
    visited = set()
    pq = [(0, start, [start])]
    costs = {start: 0}

    print("\n" + "="*60)
    print("UCS - Búsqueda de Costo Uniforme")
    print("="*60)
    print(f"Nodo inicio: {start} | Nodo meta: {goal}\n")

    plt.ion()
    plt.figure(figsize=(10,7))  # figura única

    step = 1
    while pq:
        cost, node, path = heapq.heappop(pq)
        print(f"Paso {step}: Nodo: {node} | Costo: {cost} | Camino: {' → '.join(path)}")

        if node == goal:
            print(f"UCS COMPLETO! Camino: {' → '.join(path)} | Costo total: {cost}")
            graph.draw(path=path, current=node, algo_name="UCS COMPLETADO")
            plt.ioff()
            plt.show()
            return path

        if node not in visited:
            visited.add(node)

            for neighbor in sorted(graph.G.neighbors(node)):
                weight = graph.G.edges[node, neighbor]['weight']
                new_cost = cost + weight
                if neighbor not in costs or new_cost < costs[neighbor]:
                    costs[neighbor] = new_cost
                    heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))

            graph.draw(visited=list(visited), path=path, current=node, structure=[n for _, n, _ in pq], algo_name="UCS")
            time.sleep(delay)
            step += 1

    print(f"No se encontró camino desde {start} hasta {goal}")
    plt.ioff()
    plt.show()
    return None

# Grafo de ejemplo

def example_graph() -> GraphVisualizer:
    g = GraphVisualizer()
    edges = [
        ('S','A',3), ('S','B',2), ('A','B',2), ('A','C',1),
        ('B','C',5), ('C','D',1), ('B','D',4), ('D','E',2),
        ('C','F',7), ('D','F',8), ('F','G',1)
    ]
    for u,v,w in edges:
        g.add_edge(u,v,w)
    positions = {
        'S':(0,2), 'A':(-1,1), 'B':(0,0), 'C':(1,1),
        'D':(1.5,0), 'E':(2.5,1), 'F':(2,-1), 'G':(3,-1)
    }
    g.set_positions(positions)
    return g

# Menú interactivo
def menu_grafos():
    g = example_graph()

    while True:
        print("MENU GRAFOS")
        print("  1. DFS - Búsqueda en Profundidad")
        print("  2. BFS - Búsqueda en Anchura")
        print("  3. UCS - Búsqueda de Costo Uniforme")
        print("  0. Salir")

        choice = input("Elige una opción: ").strip()
        if choice == '1':
            dfs_step_by_step(g, 'S', delay=1.0)
        elif choice == '2':
            bfs_step_by_step(g, 'S', delay=1.0)
        elif choice == '3':
            start = input("Nodo inicio (default 'S'): ").strip().upper() or 'S'
            goal = input("Nodo meta (default 'G'): ").strip().upper() or 'G'
            ucs_step_by_step(g, start, goal, delay=1.0)
        elif choice == '0':
            print("\nHasta luego!\n")
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    menu_grafos()
