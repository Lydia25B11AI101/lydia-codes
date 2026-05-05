/* Program Title: LRU Cache (Doubly Linked List + Hash Map)
   Author: Lydia S. Makiwa
   Date: 2026-05-05
   Description: Implements an LRU (Least Recently Used) Cache using
                a doubly linked list + hash map approach.
                Used in operating systems, CPU caches, and web browsers. */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CAPACITY 4

typedef struct Node {
    int key, val;
    struct Node *prev, *next;
} Node;

typedef struct {
    Node* map[100];   // simple direct-mapped "hash" (keys 0-99)
    Node* head;       // most recently used
    Node* tail;       // least recently used
    int   size;
    int   cap;
} LRUCache;

Node* new_node(int k, int v) {
    Node* n = malloc(sizeof(Node));
    n->key=k; n->val=v; n->prev=n->next=NULL;
    return n;
}

void move_to_front(LRUCache* c, Node* n) {
    if (n == c->head) return;
    // Detach
    if (n->prev) n->prev->next = n->next;
    if (n->next) n->next->prev = n->prev;
    if (n == c->tail) c->tail = n->prev;
    // Prepend
    n->prev = NULL; n->next = c->head;
    if (c->head) c->head->prev = n;
    c->head = n;
    if (!c->tail) c->tail = n;
}

void lru_put(LRUCache* c, int k, int v) {
    if (c->map[k]) {
        c->map[k]->val = v;
        move_to_front(c, c->map[k]);
        return;
    }
    Node* n = new_node(k, v);
    c->map[k] = n;
    // Prepend to head
    n->next = c->head;
    if (c->head) c->head->prev = n;
    c->head = n;
    if (!c->tail) c->tail = n;
    c->size++;
    // Evict LRU if over capacity
    if (c->size > c->cap) {
        printf("  [EVICT] key=%d\n", c->tail->key);
        c->map[c->tail->key] = NULL;
        Node* old = c->tail;
        c->tail = c->tail->prev;
        if (c->tail) c->tail->next = NULL;
        free(old); c->size--;
    }
}

int lru_get(LRUCache* c, int k) {
    if (!c->map[k]) return -1;
    move_to_front(c, c->map[k]);
    return c->map[k]->val;
}

void print_cache(LRUCache* c) {
    printf("  Cache (MRU→LRU): ");
    Node* cur = c->head;
    while (cur) { printf("[%d:%d] ", cur->key, cur->val); cur=cur->next; }
    printf("\n");
}

int main() {
    LRUCache c; memset(&c, 0, sizeof(c)); c.cap = CAPACITY;
    printf("=== LRU Cache (capacity=%d) ===\n\n", CAPACITY);
    int ops[][2] = {1,10,{2,20},{3,30},{4,40},{1,0},{5,50},{2,0},{3,0}};
    // Manual demonstration
    lru_put(&c,1,10); print_cache(&c);
    lru_put(&c,2,20); print_cache(&c);
    lru_put(&c,3,30); print_cache(&c);
    lru_put(&c,4,40); print_cache(&c);
    printf("  GET key=1 → %d\n", lru_get(&c,1)); print_cache(&c);
    lru_put(&c,5,50); print_cache(&c);  // evicts LRU
    printf("  GET key=2 → %d (evicted=-1)\n", lru_get(&c,2));
    printf("  GET key=3 → %d\n", lru_get(&c,3));
    print_cache(&c);
    return 0;
}
