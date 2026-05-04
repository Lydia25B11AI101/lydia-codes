/* ============================================================
 * Program Title : Hash Table with Separate Chaining
 * Author        : Lydia S. Makiwa
 * Date          : 2026-05-04
 * Description   : Implement a hash table using linked-list
 *                 chaining for collision resolution.
 * ============================================================ */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TABLE_SIZE 10

typedef struct Node {
    char key[50];
    int  value;
    struct Node *next;
} Node;

Node *table[TABLE_SIZE];

int hash(const char *key) {
    int h = 0;
    while (*key) h = (h*31 + *key++) % TABLE_SIZE;
    return h;
}

void insert(const char *key, int value) {
    int idx = hash(key);
    Node *n = malloc(sizeof(Node));
    strcpy(n->key, key);
    n->value = value;
    n->next  = table[idx];
    table[idx] = n;
}

int search(const char *key) {
    Node *cur = table[hash(key)];
    while (cur) {
        if (strcmp(cur->key, key)==0) return cur->value;
        cur = cur->next;
    }
    return -1;
}

int main() {
    memset(table, 0, sizeof(table));
    insert("alice",  25);
    insert("bob",    30);
    insert("charlie",22);
    insert("diana",  28);
    insert("eve",    35);
    char *names[] = {"alice","bob","charlie","zara"};
    for (int i=0;i<4;i++) {
        int v = search(names[i]);
        if (v==-1) printf("%s: not found\n", names[i]);
        else        printf("%s: age=%d\n",   names[i], v);
    }
    printf("Hash table demo complete!\n");
    return 0;
}
