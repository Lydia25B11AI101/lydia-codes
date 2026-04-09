/*
 * Program Title : Doubly Linked List Operations
 * Author        : Lydia S. Makiwa
 * Date          : 2026-04-09
 * Description   : Implements a doubly linked list with insert,
 *                 delete, forward/backward traversal in C.
 *                 Covers: structs, malloc, pointers.
 */

#include <stdio.h>
#include <stdlib.h>

/* Node structure: has pointers to BOTH next and previous nodes */
typedef struct Node {
    int data;
    struct Node* next;
    struct Node* prev;
} Node;

/* Create a new node */
Node* create_node(int data) {
    Node* node = (Node*)malloc(sizeof(Node));
    node->data = data;
    node->next = NULL;
    node->prev = NULL;
    return node;
}

/* Insert at the end */
void insert_end(Node** head, int data) {
    Node* new_node = create_node(data);
    if (*head == NULL) {
        *head = new_node;
        return;
    }
    Node* temp = *head;
    while (temp->next != NULL)
        temp = temp->next;
    temp->next   = new_node;
    new_node->prev = temp;
}

/* Delete a node by value */
void delete_node(Node** head, int data) {
    Node* temp = *head;
    while (temp != NULL && temp->data != data)
        temp = temp->next;
    if (temp == NULL) { printf("Value %d not found.\n", data); return; }
    if (temp->prev != NULL) temp->prev->next = temp->next;
    else                    *head = temp->next;
    if (temp->next != NULL) temp->next->prev = temp->prev;
    free(temp);
    printf("Deleted %d\n", data);
}

/* Print forward */
void print_forward(Node* head) {
    printf("Forward : ");
    while (head != NULL) { printf("%d ", head->data); head = head->next; }
    printf("\n");
}

/* Print backward */
void print_backward(Node* head) {
    if (head == NULL) return;
    while (head->next != NULL) head = head->next;
    printf("Backward: ");
    while (head != NULL) { printf("%d ", head->data); head = head->prev; }
    printf("\n");
}

int main() {
    Node* head = NULL;
    int values[] = {10, 20, 30, 40, 50};
    int n = sizeof(values) / sizeof(values[0]);

    printf("=== Doubly Linked List Demo ===\n");
    for (int i = 0; i < n; i++) insert_end(&head, values[i]);

    print_forward(head);
    print_backward(head);

    delete_node(&head, 30);
    print_forward(head);

    delete_node(&head, 99);  /* not found */
    return 0;
}
