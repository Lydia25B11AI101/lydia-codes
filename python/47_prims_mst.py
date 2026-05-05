# Program Title: Prim's Minimum Spanning Tree (Greedy)
# Author: Lydia S. Makiwa
# Date: 2026-05-05
# Description: Implements Prim's algorithm to find the MST of a weighted graph.

import heapq

def prims_mst(graph, start):
    """
    graph: dict of {node: [(neighbour, weight), ...]}
    Returns total MST weight and list of edges chosen.
    """
    visited = set()
    min_heap = [(0, start, None)]   # (weight, node, parent)
    mst_edges = []
    total_cost = 0

    while min_heap:
        weight, node, parent = heapq.heappop(min_heap)
        if node in visited:
            continue
        visited.add(node)
        total_cost += weight
        if parent is not None:
            mst_edges.append((parent, node, weight))

        for neighbour, w in graph.get(node, []):
            if neighbour not in visited:
                heapq.heappush(min_heap, (w, neighbour, node))

    return total_cost, mst_edges

# ─── Demo ───
graph = {
    'A': [('B', 2), ('C', 3)],
    'B': [('A', 2), ('C', 1), ('D', 4)],
    'C': [('A', 3), ('B', 1), ('D', 5)],
    'D': [('B', 4), ('C', 5)]
}

cost, edges = prims_mst(graph, 'A')
print(f"Prim's MST Total Cost: {cost}")
print("MST Edges:")
for u, v, w in edges:
    print(f"  {u} --{w}--> {v}")
