# Data Structure 9: Graph — BFS and DFS Traversal
# Author: Lydia S. Makiwa
# Description: Adjacency list graph with Breadth-First and Depth-First Search

from collections import deque

class Graph:
    def __init__(self):
        self.adj = {}

    def add_vertex(self, v):
        if v not in self.adj:
            self.adj[v] = []

    def add_edge(self, u, v):
        self.add_vertex(u); self.add_vertex(v)
        self.adj[u].append(v)
        self.adj[v].append(u)  # undirected

    def bfs(self, start):
        visited = set([start])
        queue   = deque([start])
        order   = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbour in self.adj[node]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
        return order

    def dfs(self, start, visited=None):
        if visited is None: visited = set()
        visited.add(start)
        order = [start]
        for neighbour in self.adj[start]:
            if neighbour not in visited:
                order += self.dfs(neighbour, visited)
        return order

    def display(self):
        print("Adjacency List:")
        for v, edges in self.adj.items():
            print(f"  {v} → {edges}")

# Demo
g = Graph()
edges = [(1,2),(1,3),(2,4),(2,5),(3,6),(3,7)]
for u, v in edges:
    g.add_edge(u, v)

g.display()
print(f"\nBFS from node 1: {g.bfs(1)}")
print(f"DFS from node 1: {g.dfs(1)}")
