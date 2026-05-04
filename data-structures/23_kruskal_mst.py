# ============================================================
# Program Title : Kruskal's Minimum Spanning Tree
# Author        : Lydia S. Makiwa
# Date          : 2026-05-04
# Description   : Find the MST of a weighted undirected graph
#                 using Kruskal's algorithm with Union-Find.
# ============================================================

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank   = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry: return False
        if self.rank[rx] < self.rank[ry]: rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]: self.rank[rx] += 1
        return True

def kruskal(n, edges):
    edges.sort(key=lambda e: e[2])
    uf  = UnionFind(n)
    mst = []
    for u, v, w in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
        if len(mst) == n-1:
            break
    return mst

# Demo: 7 nodes, 11 edges
edges = [
    (0,1,7),(0,3,5),(1,2,8),(1,3,9),(1,4,7),
    (2,4,5),(3,4,15),(3,5,6),(4,5,8),(4,6,9),(5,6,11)
]
mst = kruskal(7, edges)
total = sum(w for _,_,w in mst)
print('MST edges:')
for u,v,w in mst:
    print(f'  {u} -- {v}  weight={w}')
print(f'Total MST weight: {total}')
print('Kruskal MST complete!')
