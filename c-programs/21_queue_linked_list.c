/* ============================================================
   Program Title : Queue using Linked List
   Author        : Lydia S. Makiwa
   Date          : 2026-05-02
   Description   : FIFO queue implementation using dynamic
                   linked list -- enqueue, dequeue, peek.
   ============================================================ */

#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node* next;
} Node;

typedef struct {
    Node* front;
    Node* rear;
    int   size;
} Queue;

void init(Queue* q)   { q->front = q->rear = NULL; q->size = 0; }
int  isEmpty(Queue* q){ return q->front == NULL; }

void enqueue(Queue* q, int val) {
    Node* n = (Node*)malloc(sizeof(Node));
    n->data = val; n->next = NULL;
    if (isEmpty(q)) q->front = q->rear = n;
    else { q->rear->next = n; q->rear = n; }
    q->size++;
    printf("  Enqueued: %d\n", val);
}

int dequeue(Queue* q) {
    if (isEmpty(q)) { printf("  Queue is empty!\n"); return -1; }
    Node* tmp = q->front;
    int val   = tmp->data;
    q->front  = q->front->next;
    if (!q->front) q->rear = NULL;
    free(tmp);
    q->size--;
    return val;
}

void printQueue(Queue* q) {
    printf("  Queue (front->rear): ");
    Node* cur = q->front;
    while (cur) { printf("%d ", cur->data); cur = cur->next; }
    printf("(size=%d)\n", q->size);
}

int main() {
    Queue q;
    init(&q);

    printf("\n=== Queue Demo ===\n");
    enqueue(&q, 10); enqueue(&q, 20);
    enqueue(&q, 30); enqueue(&q, 40);
    printQueue(&q);

    printf("  Dequeued: %d\n", dequeue(&q));
    printf("  Dequeued: %d\n", dequeue(&q));
    printQueue(&q);
    return 0;
}
