"""
Program Title: Tarjan's Strongly Connected Components (SCC)
Author: Lydia S. Makiwa
Date: June 2, 2026

Description:
An implementation of Tarjan's algorithm that detects Strongly Connected Components
(cycles where every vertex is reachable from any other vertex) in a directed graph.
Achieves linear time complexity O(V + E) using Depth-First Search (DFS) tracking.
"""

from collections import defaultdict

class TarjanSCC:
    def __init__(self, vertices_count):
        self.V = vertices_count
        self.graph = defaultdict(list)
        self.time = 0
        self.scc_list = []
        
    def add_edge(self, u, v):
        self.graph[u].append(v)
        
    def _scc_util(self, u, low, disc, stack_member, st):
        # Initialize discovery time and low value
        disc[u] = self.time
        low[u] = self.time
        self.time += 1
        stack_member[u] = True
        st.append(u)
        
        # Go through all vertices adjacent to this
        for v in self.graph[u]:
            # If v is not visited yet, recurse for it
            if disc[v] == -1:
                self._scc_util(v, low, disc, stack_member, st)
                # Check if the subtree rooted with 'v' has a connection to one of the ancestors of 'u'
                low[u] = min(low[u], low[v])
            elif stack_member[v]:
                # Update low value of 'u' only if 'v' is still in the stack
                low[u] = min(low[u], disc[v])
                
        # Head node found, pop stack and print the SCC
        w = -1
        if low[u] == disc[u]:
            current_scc = []
            while w != u:
                w = st.pop()
                current_scc.append(w)
                stack_member[w] = False
            self.scc_list.append(current_scc)

    def find_sccs(self):
        # Mark all the vertices as not visited
        disc = [-1] * self.V
        low = [-1] * self.V
        stack_member = [False] * self.V
        st = []
        
        # Call the recursive helper function to find SCCs
        for i in range(self.V):
            if disc[i] == -1:
                self._scc_util(i, low, disc, stack_member, st)
                
        return self.scc_list

# --- Working Demo ---
if __name__ == "__main__":
    print("--- Tarjan's Strongly Connected Components Algorithm ---")
    
    # Initialize a graph with 7 vertices (0 to 6)
    g = TarjanSCC(7)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0) # Back-edge forming SCC {0, 1, 2}
    g.add_edge(1, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 3) # Back-edge forming SCC {3, 4, 5}
    g.add_edge(5, 6) # Single vertex SCC {6}
    
    print("\nGraph Adjacency List:")
    for vertex in range(7):
        print(f"  Vertex {vertex} -> {g.graph[vertex]}")
        
    sccs = g.find_sccs()
    
    print(f"\nStrongly Connected Components Found: {len(sccs)}")
    for idx, scc in enumerate(sccs):
        print(f"  SCC {idx + 1}: {sorted(scc)}")