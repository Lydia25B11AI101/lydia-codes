/* C Program 15: Linked List (Singly)
   Author: Lydia S. Makiwa
   Description: Insert, delete, display singly linked list in C */

#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node* next;
};

struct Node* create_node(int data) {
    struct Node* node = (struct Node*)malloc(sizeof(struct Node));
    node->data = data;
    node->next = NULL;
    return node;
}

struct Node* insert_front(struct Node* head, int data) {
    struct Node* node = create_node(data);
    node->next = head;
    return node;
}

struct Node* delete_node(struct Node* head, int data) {
    if (!head) return NULL;
    if (head->data == data) {
        struct Node* temp = head->next;
        free(head);
        return temp;
    }
    struct Node* curr = head;
    while (curr->next && curr->next->data != data)
        curr = curr->next;
    if (curr->next) {
        struct Node* temp = curr->next;
        curr->next = temp->next;
        free(temp);
    }
    return head;
}

void display(struct Node* head) {
    while (head) {
        printf("%d -> ", head->data);
        head = head->next;
    }
    printf("NULL\n");
}

int length(struct Node* head) {
    int count = 0;
    while (head) { count++; head = head->next; }
    return count;
}

int main() {
    struct Node* head = NULL;
    int values[] = {10, 20, 30, 40, 50};
    for (int i = 0; i < 5; i++)
        head = insert_front(head, values[i]);

    printf("Linked List: "); display(head);
    printf("Length: %d\n", length(head));

    head = delete_node(head, 30);
    printf("After deleting 30: "); display(head);

    return 0;
}
