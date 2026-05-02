/* ============================================================
   Program Title : Graph BFS & DFS (Adjacency List)
   Author        : Lydia S. Makiwa
   Date          : 2026-05-02
   Description   : Breadth-First and Depth-First traversal on
                   an undirected graph using adjacency lists.
   ============================================================ */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX 10

typedef struct ANode {
    int vertex;
    struct ANode* next;
} ANode;

ANode* graph[MAX];
int    visited[MAX];

ANode* newNode(int v) {
    ANode* n = malloc(sizeof(ANode));
    n->vertex = v; n->next = NULL;
    return n;
}

void addEdge(int u, int v) {
    ANode* n = newNode(v);
    n->next = graph[u]; graph[u] = n;
    n = newNode(u);
    n->next = graph[v]; graph[v] = n;
}

/* BFS -- level-order traversal */
void bfs(int start, int n) {
    int queue[MAX], front = 0, rear = 0;
    memset(visited, 0, sizeof(visited));
    visited[start] = 1;
    queue[rear++] = start;
    printf("BFS: ");
    while (front < rear) {
        int v = queue[front++];
        printf("%d ", v);
        for (ANode* t = graph[v]; t; t = t->next)
            if (!visited[t->vertex]) {
                visited[t->vertex] = 1;
                queue[rear++] = t->vertex;
            }
    }
    printf("\n");
}

/* DFS -- recursive */
void dfs(int v) {
    visited[v] = 1;
    printf("%d ", v);
    for (ANode* t = graph[v]; t; t = t->next)
        if (!visited[t->vertex]) dfs(t->vertex);
}

int main() {
    int n = 6;
    for (int i = 0; i < n; i++) graph[i] = NULL;

    addEdge(0, 1); addEdge(0, 2);
    addEdge(1, 3); addEdge(2, 4);
    addEdge(3, 5); addEdge(4, 5);

    bfs(0, n);

    memset(visited, 0, sizeof(visited));
    printf("DFS: "); dfs(0); printf("\n");
    return 0;
}
