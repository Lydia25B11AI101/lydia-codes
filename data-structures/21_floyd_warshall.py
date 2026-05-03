# ============================================================
# Program Title : Floyd-Warshall All-Pairs Shortest Paths
# Author        : Lydia S. Makiwa
# Date          : 2026-05-03
# Description   : Computes shortest distances between every pair
#                 of vertices in O(V³) — handles negative edges.
# ============================================================

INF = float('inf')

def floyd_warshall(graph: list[list]) -> tuple:
    """
    Args:
        graph: V×V adjacency matrix (INF if no direct edge).
    Returns:
        (dist, next_node) matrices for distances and path reconstruction.
    """
    V    = len(graph)
    dist = [row[:] for row in graph]           # deep copy
    nxt  = [[j if graph[i][j] != INF else -1
              for j in range(V)] for i in range(V)]

    for k in range(V):
        for i in range(V):
            for j in range(V):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j]  = nxt[i][k]

    # Detect negative cycles
    for i in range(V):
        if dist[i][i] < 0:
            raise ValueError("Graph contains a negative weight cycle!")

    return dist, nxt

def reconstruct_path(nxt: list, src: int, dst: int) -> list:
    """Return list of vertices on the shortest path from src to dst."""
    if nxt[src][dst] == -1:
        return []
    path = [src]
    while src != dst:
        src = nxt[src][dst]
        path.append(src)
    return path

# ── Demo ─────────────────────────────────────────────────────
if __name__ == "__main__":
    V = 4
    I = INF
    # Adjacency matrix (0-indexed vertices)
    graph = [
        [0, 3, I, 7],
        [8, 0, 2, I],
        [5, I, 0, 1],
        [2, I, I, 0],
    ]

    dist, nxt = floyd_warshall(graph)

    print("Floyd-Warshall All-Pairs Shortest Paths")
    print("=" * 42)
    print("Distance matrix:")
    header = "     " + "  ".join(f" {j:3d}" for j in range(V))
    print(header)
    for i in range(V):
        row = f"  {i}: " + "  ".join(
            f"{d:4d}" if d != INF else " INF" for d in dist[i])
        print(row)

    print("\nShortest paths:")
    for s in range(V):
        for d in range(V):
            if s != d and dist[s][d] != INF:
                path = reconstruct_path(nxt, s, d)
                print(f"  {s} → {d} | dist={dist[s][d]} | path={' → '.join(map(str,path))}")
