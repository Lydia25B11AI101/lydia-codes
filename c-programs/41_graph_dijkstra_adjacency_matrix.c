/* ==============================================================================
 * Title: Dijkstra's Shortest Path Algorithm using Adjacency Matrix
 * Author: Lydia S. Makiwa
 * Date: June 3, 2026
 * Description: Solves the single-source shortest path problem for a weighted directed/undirected 
 *              graph represented as an adjacency matrix. Outputs the shortest distance and the 
 *              exact path from the source vertex to all other vertices.
 * ==============================================================================
 */

#include <stdio.h>
#include <stdbool.h>

#define V 6       // Number of vertices in the graph
#define INF 99999 // Represent Infinity

// Utility to find the vertex with the minimum distance value from set of unvisited vertices
int minDistance(int dist[], bool visited[]) {
    int min = INF, min_index;
    for (int v = 0; v < V; v++) {
        if (!visited[v] && dist[v] <= min) {
            min = dist[v];
            min_index = v;
        }
    }
    return min_index;
}

// Utility to print shortest path recursively
void printPath(int parent[], int j) {
    if (parent[j] == -1) {
        printf("%d", j);
        return;
    }
    printPath(parent, parent[j]);
    printf(" -> %d", j);
}

// Print final distance matrix and paths
void printSolution(int dist[], int parent[], int src) {
    printf("\nShortest Paths from Source Vertex %d:\n", src);
    printf("%-10s %-10s %-25s\n", "Vertex", "Distance", "Shortest Path");
    for (int i = 0; i < V; i++) {
        if (dist[i] == INF) {
            printf("%-10d %-10s %-25s\n", i, "INF", "No path");
        } else {
            printf("%-10d %-10d ", i, dist[i]);
            printPath(parent, i);
            printf("\n");
        }
    }
}

// Dijkstra Algorithm
void dijkstra(int graph[V][V], int src) {
    int dist[V];     // Holds shortest distance from src to i
    bool visited[V]; // visited[i] will be true if vertex i is finalized
    int parent[V];   // Parent array to store shortest path reconstruction

    // Initialize all distances as INF, visited as false, parent as -1
    for (int i = 0; i < V; i++) {
        dist[i] = INF;
        visited[i] = false;
        parent[i] = -1;
    }

    // Distance of source vertex from itself is always 0
    dist[src] = 0;

    // Find shortest path for all vertices
    for (int count = 0; count < V - 1; count++) {
        // Pick the minimum distance vertex
        int u = minDistance(dist, visited);
        visited[u] = true;

        // Update dist value of adjacent vertices of picked vertex
        for (int v = 0; v < V; v++) {
            // Update dist[v] only if it's not visited, there's an edge,
            // and total weight of path through u is smaller than current dist[v]
            if (!visited[v] && graph[u][v] && dist[u] != INF && dist[u] + graph[u][v] < dist[v]) {
                parent[v] = u;
                dist[v] = dist[u] + graph[u][v];
            }
        }
    }

    printSolution(dist, parent, src);
}

// Working example
int main() {
    printf("--- Dijkstra's Shortest Path Demo (Adjacency Matrix) ---\n");

    // Adjacency Matrix representing a graph where graph[i][j] is the edge weight
    // 0 represents no edge between vertices i and j
    int graph[V][V] = {
        {0, 4, 2, 0, 0, 0}, // Edges from Node 0
        {0, 0, 1, 5, 0, 0}, // Edges from Node 1
        {0, 0, 0, 8, 10, 0},// Edges from Node 2
        {0, 0, 0, 0, 2, 6}, // Edges from Node 3
        {0, 0, 0, 0, 0, 3}, // Edges from Node 4
        {0, 0, 0, 0, 0, 0}  // Edges from Node 5
    };

    int source = 0;
    dijkstra(graph, source);

    return 0;
}
