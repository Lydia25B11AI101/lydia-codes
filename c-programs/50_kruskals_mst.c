/*
 * Program: Kruskal's Minimum Spanning Tree using Disjoint Set Union (DSU)
 * Author: Lydia S. Makiwa
 * Date: June 7, 2026
 * Category: Data Structures & Algorithms / C Programming
 *
 * Description:
 * Implements Kruskal's greedy algorithm to find the Minimum Spanning Tree (MST)
 * of a connected, undirected, weighted graph. It makes use of a fast Disjoint
 * Set Union (DSU) structure with both Union by Rank and Path Compression.
 */
#include <stdio.h>
#include <stdlib.h>

// Structure to represent an edge in the graph
struct Edge {
    int src, dest, weight;
};

// Structure to represent a connected, undirected, weighted graph
struct Graph {
    int V, E;
    struct Edge* edge;
};

// Structure to represent subset elements for DSU
struct Subset {
    int parent;
    int rank;
};

// Function to create a graph with V vertices and E edges
struct Graph* createGraph(int V, int E) {
    struct Graph* graph = (struct Graph*)malloc(sizeof(struct Graph));
    graph->V = V;
    graph->E = E;
    graph->edge = (struct Edge*)malloc(graph->E * sizeof(struct Edge));
    return graph;
}

// Find set of an element i (uses path compression)
int find(struct Subset subsets[], int i) {
    if (subsets[i].parent != i) {
        subsets[i].parent = find(subsets, subsets[i].parent);
    }
    return subsets[i].parent;
}

// Union of two sets by rank
void Union(struct Subset subsets[], int x, int y) {
    int xroot = find(subsets, x);
    int yroot = find(subsets, y);

    if (subsets[xroot].rank < subsets[yroot].rank) {
        subsets[xroot].parent = yroot;
    } else if (subsets[xroot].rank > subsets[yroot].rank) {
        subsets[yroot].parent = xroot;
    } else {
        subsets[yroot].parent = xroot;
        subsets[xroot].rank++;
    }
}

// Compare function for qsort to sort edges by weight
int compareEdges(const void* a, const void* b) {
    struct Edge* a_edge = (struct Edge*)a;
    struct Edge* b_edge = (struct Edge*)b;
    return a_edge->weight - b_edge->weight;
}

// Kruskal's MST solver
void KruskalMST(struct Graph* graph) {
    int V = graph->V;
    struct Edge result[V]; // Stores the constructed MST edges
    int e = 0;             // Index variable used for result[]
    int i = 0;             // Index variable used for sorted edges

    // Step 1: Sort all edges in non-decreasing order of weight
    qsort(graph->edge, graph->E, sizeof(graph->edge[0]), compareEdges);

    // Allocate memory for creating V subsets
    struct Subset* subsets = (struct Subset*)malloc(V * sizeof(struct Subset));

    // Create V subsets with single elements
    for (int v = 0; v < V; ++v) {
        subsets[v].parent = v;
        subsets[v].rank = 0;
    }

    // Number of edges to be taken is equal to V-1
    while (e < V - 1 && i < graph->E) {
        // Step 2: Pick the smallest edge
        struct Edge next_edge = graph->edge[i++];

        int x = find(subsets, next_edge.src);
        int y = find(subsets, next_edge.dest);

        // If including this edge doesn't cause cycle, include it
        if (x != y) {
            result[e++] = next_edge;
            Union(subsets, x, y);
        }
    }

    // Print the constructed MST
    printf("Edges in the constructed Minimum Spanning Tree:\n");
    int minimumCost = 0;
    for (i = 0; i < e; ++i) {
        printf("%d -- %d == %d\n", result[i].src, result[i].dest, result[i].weight);
        minimumCost += result[i].weight;
    }
    printf("\nMinimum Cost of Spanning Tree: %d\n", minimumCost);

    free(subsets);
}

int main() {
    printf("=== Kruskal\'s Minimum Spanning Tree (MST) ===\n\n");

    /* Create the following weighted graph:
             10
        0 -------- 1
        | \        |
       6|   \5     |15
        |     \    |
        2 -------- 3
             4       */
    int V = 4; // Number of vertices
    int E = 5; // Number of edges
    struct Graph* graph = createGraph(V, E);

    // add edge 0-1
    graph->edge[0].src = 0;
    graph->edge[0].dest = 1;
    graph->edge[0].weight = 10;

    // add edge 0-2
    graph->edge[1].src = 0;
    graph->edge[1].dest = 2;
    graph->edge[1].weight = 6;

    // add edge 0-3
    graph->edge[2].src = 0;
    graph->edge[2].dest = 3;
    graph->edge[2].weight = 5;

    // add edge 1-3
    graph->edge[3].src = 1;
    graph->edge[3].dest = 3;
    graph->edge[3].weight = 15;

    // add edge 2-3
    graph->edge[4].src = 2;
    graph->edge[4].dest = 3;
    graph->edge[4].weight = 4;

    KruskalMST(graph);

    free(graph->edge);
    free(graph);
    return 0;
}
