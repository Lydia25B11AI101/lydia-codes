# ==============================================================================
# Title: Longest Path in Directed Acyclic Graph (DAG)
# Author: Lydia S. Makiwa
# Date: June 3, 2026
# Description: Finds the longest path in a Directed Acyclic Graph (DAG) starting from 
#              a source vertex. Uses Topological Sort combined with Dynamic Programming/Relaxation.
#              An essential graph algorithm for critical path analysis and scheduling.
# ==============================================================================

class Graph:
    def __init__(self, vertices):
        self.V = vertices  # Number of vertices
        self.adj = {i: [] for i in range(vertices)} # Adjacency list

    def add_edge(self, u, v, w):
        """u: source, v: destination, w: weight"""
        self.adj[u].append((v, w))

    def topological_sort_util(self, v, visited, stack):
        """Helper to recursively perform DFS for topological sorting."""
        visited[v] = True
        for neighbor, weight in self.adj[v]:
            if not visited[neighbor]:
                self.topological_sort_util(neighbor, visited, stack)
        stack.append(v)

    def find_longest_path(self, src):
        """Finds longest path from src vertex to all other reachable vertices."""
        # Step 1: Initialize distances as negative infinity (INF)
        # distance to source itself is 0
        dist = [-float('inf')] * self.V
        dist[src] = 0
        parent = [-1] * self.V

        # Step 2: Get Topological Sort of graph
        visited = [False] * self.V
        stack = []
        for i in range(self.V):
            if not visited[i]:
                self.topological_sort_util(i, visited, stack)

        # Reverse stack to get topological order
        topo_order = stack[::-1]

        # Step 3: Process vertices in topological order
        for u in topo_order:
            # If vertex u is reachable
            if dist[u] != -float('inf'):
                # Update distance for all neighbors of u
                for v, weight in self.adj[u]:
                    # Relaxation for longest path (maximize instead of minimize)
                    if dist[v] < dist[u] + weight:
                        dist[v] = dist[u] + weight
                        parent[v] = u

        return dist, parent

# --- Demo & Example ---
if __name__ == "__main__":
    print("--- Longest Path in DAG using Topological Sorting Demo ---")
    
    # Create a graph with 6 vertices (0 to 5)
    g = Graph(6)
    g.add_edge(0, 1, 5)
    g.add_edge(0, 2, 3)
    g.add_edge(1, 3, 6)
    g.add_edge(1, 2, 2)
    g.add_edge(2, 4, 4)
    g.add_edge(2, 5, 2)
    g.add_edge(2, 3, 7)
    g.add_edge(3, 5, 1)
    g.add_edge(3, 4, -1)
    g.add_edge(4, 5, -2)

    source_vertex = 1
    print(f"\nFinding longest paths in DAG from Source Vertex: {source_vertex}")
    distances, parents = g.find_longest_path(source_vertex)

    print("\nResults:")
    print(f"{'Dest Vertex':<12} {'Max Distance':<15} {'Path Path':<20}")
    for i in range(g.V):
        dist = distances[i]
        if dist == -float('inf'):
            print(f"{i:<12} {'Unreachable':<15} {'N/A':<20}")
        else:
            # Reconstruct the path
            path = []
            curr = i
            while curr != -1:
                path.append(curr)
                curr = parents[curr]
            path.reverse()
            path_str = " -> ".join(map(str, path))
            print(f"{i:<12} {dist:<15} {path_str:<20}")
