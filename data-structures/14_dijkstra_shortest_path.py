# ============================================================
# Program Title : Dijkstra's Shortest Path Algorithm
# Author        : Lydia S. Makiwa
# Date          : 2026-04-09
# Description   : Finds the shortest path from a source node
#                 to all other nodes in a weighted graph using
#                 a priority queue (min-heap). Classic graph
#                 algorithm used in GPS navigation, networking.
# ============================================================

import heapq

def dijkstra(graph, source):
    """
    Args:
        graph  : dict of {node: [(neighbour, weight), ...]}
        source : starting node
    Returns:
        dist   : dict of shortest distances from source
        prev   : dict to reconstruct paths
    """
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    prev = {node: None for node in graph}

    # Priority queue: (distance, node)
    pq = [(0, source)]

    while pq:
        current_dist, u = heapq.heappop(pq)

        # Skip if we already found a shorter path
        if current_dist > dist[u]:
            continue

        for v, weight in graph[u]:
            new_dist = dist[u] + weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(pq, (new_dist, v))

    return dist, prev

def reconstruct_path(prev, source, target):
    """Trace back the shortest path from source to target."""
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    return path if path[0] == source else []

# -- Demo --------------------------------------------------
if __name__ == "__main__":
    # Weighted undirected graph (adjacency list)
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('A', 4), ('C', 5), ('D', 10)],
        'C': [('A', 2), ('B', 5), ('E', 3)],
        'D': [('B', 10), ('E', 4), ('F', 11)],
        'E': [('C', 3), ('D', 4), ('F', 2)],
        'F': [('D', 11), ('E', 2)],
    }

    source = 'A'
    dist, prev = dijkstra(graph, source)

    print("Dijkstra's Shortest Paths from node", source)
    print("-" * 40)
    for node in sorted(graph.keys()):
        path = reconstruct_path(prev, source, node)
        path_str = " -> ".join(path)
        print(f"  {source} to {node}: distance = {dist[node]}  path = {path_str}")

    print()
    # City example
    city_graph = {
        'Home':       [('School', 5), ('Market', 3)],
        'School':     [('Home', 5), ('Library', 4), ('Park', 6)],
        'Market':     [('Home', 3), ('Park', 2)],
        'Library':    [('School', 4), ('Office', 7)],
        'Park':       [('School', 6), ('Market', 2), ('Office', 5)],
        'Office':     [('Library', 7), ('Park', 5)],
    }
    city_dist, city_prev = dijkstra(city_graph, 'Home')
    print("Shortest travel times from Home:")
    for place in sorted(city_graph.keys()):
        path = " -> ".join(reconstruct_path(city_prev, 'Home', place))
        print(f"  {place:12}: {city_dist[place]} min  [{path}]")
