/*
 * Title: Bellman-Ford Shortest Path Algorithm with Negative Cycle Detection
 * Author: Lydia S. Makiwa
 * Date: June 06, 2026
 *
 * Description:
 * This program implements the Bellman-Ford algorithm in C. It finds the single-source
 * shortest path in a weighted graph, even in the presence of negative edge weights,
 * and is capable of detecting negative weight cycles.
 * 
 * Perfect for practicing graph representation, structs, and path optimization concepts.
 */

#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#define INF 999999 // Represent infinity

struct Edge {
    int src, dest, weight;
};

struct Graph {
    int V, E;
    struct Edge* edge;
};

struct Graph* createGraph(int V, int E) {
    struct Graph* graph = (struct Graph*) malloc(sizeof(struct Graph));
    graph->V = V;
    graph->E = E;
    graph->edge = (struct Edge*) malloc(graph->E * sizeof(struct Edge));
    return graph;
}

void printSolution(int dist[], int n) {
    printf("Vertex   Distance from Source\n");
    for (int i = 0; i < n; ++i) {
        if (dist[i] == INF) {
            printf("%d \t\t INF\n", i);
        } else {
            printf("%d \t\t %d\n", i, dist[i]);
        }
    }
}

void BellmanFord(struct Graph* graph, int src) {
    int V = graph->V;
    int E = graph->E;
    int dist[V];

    // Step 1: Initialize distances from src to all other vertices as INFINITE
    for (int i = 0; i < V; i++) {
        dist[i] = INF;
    }
    dist[src] = 0;

    // Step 2: Relax all edges |V| - 1 times.
    for (int i = 1; i <= V - 1; i++) {
        for (int j = 0; j < E; j++) {
            int u = graph->edge[j].src;
            int v = graph->edge[j].dest;
            int weight = graph->edge[j].weight;
            if (dist[u] != INF && dist[u] + weight < dist[v]) {
                dist[v] = dist[u] + weight;
            }
        }
    }

    // Step 3: Check for negative-weight cycles.
    for (int j = 0; j < E; j++) {
        int u = graph->edge[j].src;
        int v = graph->edge[j].dest;
        int weight = graph->edge[j].weight;
        if (dist[u] != INF && dist[u] + weight < dist[v]) {
            printf("Graph contains negative weight cycle! Shortest path cannot be determined safely.\n");
            return;
        }
    }

    printSolution(dist, V);
}

int main() {
    printf("=== Bellman-Ford Shortest Path Algorithm ===\n");
    int V = 5; // Number of vertices
    int E = 8; // Number of edges
    struct Graph* graph = createGraph(V, E);

    // Edge 0-1
    graph->edge[0].src = 0;
    graph->edge[0].dest = 1;
    graph->edge[0].weight = -1;

    // Edge 0-2
    graph->edge[1].src = 0;
    graph->edge[1].dest = 2;
    graph->edge[1].weight = 4;

    // Edge 1-2
    graph->edge[2].src = 1;
    graph->edge[2].dest = 2;
    graph->edge[2].weight = 3;

    // Edge 1-3
    graph->edge[3].src = 1;
    graph->edge[3].dest = 3;
    graph->edge[3].weight = 2;

    // Edge 1-4
    graph->edge[4].src = 1;
    graph->edge[4].dest = 4;
    graph->edge[4].weight = 2;

    // Edge 3-2
    graph->edge[5].src = 3;
    graph->edge[5].dest = 1;
    graph->edge[5].weight = 1;

    // Edge 3-1
    graph->edge[6].src = 4;
    graph->edge[6].dest = 3;
    graph->edge[6].weight = -3;

    // Edge 2-4
    graph->edge[7].src = 2;
    graph->edge[7].dest = 4;
    graph->edge[7].weight = 5;

    BellmanFord(graph, 0);

    free(graph->edge);
    free(graph);
    return 0;
}
