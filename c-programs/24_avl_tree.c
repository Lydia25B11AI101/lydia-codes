/* ============================================================
   Program Title : AVL Tree (Self-Balancing BST)
   Author        : Lydia S. Makiwa
   Date          : 2026-05-03
   Description   : Implements an AVL Tree with insert, search,
                   and in-order traversal in C.
   ============================================================ */

#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *left, *right;
    int height;
} Node;

int height(Node *n) { return n ? n->height : 0; }
int max2(int a, int b) { return a > b ? a : b; }

int getBalance(Node *n) {
    return n ? height(n->left) - height(n->right) : 0;
}

Node *newNode(int data) {
    Node *n  = (Node*)malloc(sizeof(Node));
    n->data  = data;
    n->left  = n->right = NULL;
    n->height = 1;
    return n;
}

Node *rotateRight(Node *y) {
    Node *x  = y->left;
    Node *T2 = x->right;
    x->right = y;
    y->left  = T2;
    y->height = 1 + max2(height(y->left),  height(y->right));
    x->height = 1 + max2(height(x->left),  height(x->right));
    return x;
}

Node *rotateLeft(Node *x) {
    Node *y  = x->right;
    Node *T2 = y->left;
    y->left  = x;
    x->right = T2;
    x->height = 1 + max2(height(x->left),  height(x->right));
    y->height = 1 + max2(height(y->left),  height(y->right));
    return y;
}

Node *insert(Node *node, int data) {
    if (!node) return newNode(data);
    if (data < node->data)      node->left  = insert(node->left,  data);
    else if (data > node->data) node->right = insert(node->right, data);
    else return node;   /* duplicates ignored */

    node->height = 1 + max2(height(node->left), height(node->right));
    int bal = getBalance(node);

    /* Left-Left */
    if (bal > 1 && data < node->left->data)        return rotateRight(node);
    /* Right-Right */
    if (bal < -1 && data > node->right->data)      return rotateLeft(node);
    /* Left-Right */
    if (bal > 1 && data > node->left->data) {
        node->left = rotateLeft(node->left);
        return rotateRight(node);
    }
    /* Right-Left */
    if (bal < -1 && data < node->right->data) {
        node->right = rotateRight(node->right);
        return rotateLeft(node);
    }
    return node;
}

void inOrder(Node *root) {
    if (root) {
        inOrder(root->left);
        printf("%d ", root->data);
        inOrder(root->right);
    }
}

int main() {
    int values[] = {30, 20, 10, 25, 40, 35, 50};
    int n = sizeof(values)/sizeof(values[0]);
    Node *root = NULL;

    printf("Inserting: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", values[i]);
        root = insert(root, values[i]);
    }

    printf("\nIn-order traversal (sorted): ");
    inOrder(root);
    printf("\nTree height: %d\n", root->height);
    return 0;
}
