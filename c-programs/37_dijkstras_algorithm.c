/*
 * Program Title: Dijkstra's Single-Source Shortest Path Algorithm
 * Author: Lydia S. Makiwa
 * Date: June 2, 2026
 *
 * Description:
 * Implements Dijkstra's algorithm to compute the shortest paths from a source vertex
 * to all other vertices in a weighted graph using an adjacency matrix.
 */

#include <stdio.h>
#include <stdbool.h>
#include <limits.h>

#define V 9 // Number of vertices in the graph

// Helper function to find the vertex with the minimum distance value from the
// set of vertices not yet included in the shortest path tree
int minDistance(int dist[], bool sptSet[]) {
    int min = INT_MAX, min_index;
    
    for (int v = 0; v < V; v++) {
        if (!sptSet[v] && dist[v] <= min) {
            min = dist[v];
            min_index = v;
        }
    }
    return min_index;
}

// Function to print the constructed distance array
void printSolution(int dist[], int src) {
    printf("Vertex\t\tDistance from Source (Vertex %d)\n", src);
    for (int i = 0; i < V; i++) {
        if (dist[i] == INT_MAX) {
            printf("%d \t\t INFINITE\n", i);
        } else {
            printf("%d \t\t %d\n", i, dist[i]);
        }
    }
}

// Dijkstra's algorithm for adjacency matrix representation
void dijkstra(int graph[V][V], int src) {
    int dist[V];     // dist[i] will hold the shortest distance from src to i
    bool sptSet[V];  // sptSet[i] will be true if vertex i is included in shortest path tree
    
    // Initialize all distances as INFINITE and sptSet[] as false
    for (int i = 0; i < V; i++) {
        dist[i] = INT_MAX;
        sptSet[i] = false;
    }
    
    // Distance of source vertex from itself is always 0
    dist[src] = 0;
    
    // Find shortest path for all vertices
    for (int count = 0; count < V - 1; count++) {
        // Pick the minimum distance vertex from the set of vertices not yet processed
        int u = minDistance(dist, sptSet);
        
        // Mark the picked vertex as processed
        sptSet[u] = true;
        
        // Update dist value of the adjacent vertices of the picked vertex
        for (int v = 0; v < V; v++) {
            // Update dist[v] only if:
            // 1. It is not in sptSet
            // 2. There is an edge from u to v
            // 3. Total weight of path from src to v through u is smaller than current value of dist[v]
            if (!sptSet[v] && graph[u][v] && dist[u] != INT_MAX && dist[u] + graph[u][v] < dist[v]) {
                dist[v] = dist[u] + graph[u][v];
            }
        }
    }
    
    // Print the calculated distances
    printSolution(dist, src);
}

int main() {
    printf("--- Dijkstra's Single Source Shortest Path Algorithm ---\n\n");
    
    /* Let us create the following weighted graph
          12        8
       0 ---- 1 ---- 2
       | \    |    / |
      4|  8\  |11 /2 |9
       |    \ |  /   |
       3 ---- 4 ---- 5
       |   7  |  6   |
      8|      |14    |10
       |      |      |
       6 ---- 7 ---- 8
          2       1
    */
    int graph[V][V] = {
        {0, 12, 0, 4, 8, 0, 0, 0, 0},
        {12, 0, 8, 0, 11, 0, 0, 0, 0},
        {0, 8, 0, 0, 2, 9, 0, 0, 0},
        {4, 0, 0, 0, 7, 0, 8, 0, 0},
        {8, 11, 2, 7, 0, 6, 0, 14, 0},
        {0, 0, 9, 0, 6, 0, 0, 0, 10},
        {0, 0, 0, 8, 0, 0, 0, 2, 0},
        {0, 0, 0, 0, 14, 0, 2, 0, 1},
        {0, 0, 0, 0, 0, 10, 0, 1, 0}
    };
    
    int source_vertex = 0;
    dijkstra(graph, source_vertex);
    
    return 0;
}