# ============================================================
# Program Title : Bellman-Ford Shortest Path
# Author        : Lydia S. Makiwa
# Date          : 2026-05-02
# Description   : Finds shortest paths from a source vertex;
#                 also detects negative-weight cycles.
# ============================================================

def bellman_ford(vertices, edges, source):
    # Step 1: initialise distances
    dist = {v: float('inf') for v in vertices}
    dist[source] = 0
    parent = {v: None for v in vertices}

    # Step 2: relax edges |V| - 1 times
    for _ in range(len(vertices) - 1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u

    # Step 3: check for negative cycles
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            return None, None   # negative cycle detected

    return dist, parent


def reconstruct_path(parent, target):
    path = []
    cur  = target
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    return path[::-1]


# -- Demo ------------------------------------------------------
if __name__ == "__main__":
    vertices = list("ABCDE")
    edges = [
        ("A","B", 4), ("A","C", 2),
        ("B","C", 5), ("B","D", 10),
        ("C","E", 3), ("D","B", -2),
        ("E","D", 4),
    ]

    dist, parent = bellman_ford(vertices, edges, "A")
    if dist is None:
        print("Negative cycle detected!")
    else:
        print("Shortest distances from A:")
        for v, d in dist.items():
            path = " -> ".join(reconstruct_path(parent, v))
            print(f"  A -> {v}: {d}  (path: {path})")
