# Program Title: Disjoint Set Union (Union-Find with Path Compression)
# Author: Lydia S. Makiwa
# Date: 2026-05-05
# Description: Implements Union-Find with union-by-rank and path compression.
#              Used in Kruskal's MST, cycle detection, network connectivity.

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank   = [0] * n
        self.components = n

    def find(self, x):
        """Path compression — flattens the tree."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """Union by rank — keeps tree shallow."""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False  # Already in same set → cycle!
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.components -= 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)

def has_cycle(n, edges):
    """Detect cycle in undirected graph using DSU."""
    dsu = DSU(n)
    for u, v in edges:
        if not dsu.union(u, v):
            return True, (u, v)
    return False, None

# ─── Demo 1: Network connectivity ───
print("=== Network Connectivity ===")
dsu = DSU(6)
connections = [(0,1),(1,2),(3,4)]
for u, v in connections:
    dsu.union(u, v)
    print(f"  Connected {u}-{v}")

pairs = [(0,2),(0,3),(4,5),(3,5)]
for a, b in pairs:
    print(f"  {a} and {b} connected? {dsu.connected(a,b)}")

print(f"  Total components: {dsu.components}")

# ─── Demo 2: Cycle detection ───
print("\n=== Cycle Detection ===")
graph_with_cycle    = [(0,1),(1,2),(2,0),(3,4)]
graph_without_cycle = [(0,1),(1,2),(2,3),(3,4)]

cycle, edge = has_cycle(5, graph_with_cycle)
print(f"  Graph with cycle:    cycle={cycle}, closing edge={edge}")

cycle, edge = has_cycle(5, graph_without_cycle)
print(f"  Graph without cycle: cycle={cycle}")
