/*
 * Program Title: Binary Search Tree (BST) Operations and Traversals
 * Author: Lydia S. Makiwa
 * Date: June 5, 2026
 * Description: A complete dynamic Binary Search Tree implementation in C.
 *              Includes insertion, searching, Inorder, Preorder, Postorder traversals,
 *              and safe heap memory deallocation to prevent leaks.
 *              Essential study material for AIML students exploring memory management.
 */

#include <stdio.h>
#include <stdlib.h>

// BST Node structure
struct Node {
    int data;
    struct Node* left;
    struct Node* right;
};

// Function to create a new BST node
struct Node* createNode(int value) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    if (newNode == NULL) {
        printf("Memory allocation failed!\n");
        exit(1);
    }
    newNode->data = value;
    newNode->left = NULL;
    newNode->right = NULL;
    return newNode;
}

// Insert a node into BST recursively
struct Node* insert(struct Node* root, int value) {
    if (root == NULL) {
        return createNode(value);
    }
    if (value < root->data) {
        root->left = insert(root->left, value);
    } else if (value > root->data) {
        root->right = insert(root->right, value);
    }
    return root;
}

// Search for a value in BST
struct Node* search(struct Node* root, int key) {
    if (root == NULL || root->data == key) {
        return root;
    }
    if (key < root->data) {
        return search(root->left, key);
    }
    return search(root->right, key);
}

// Inorder traversal: Left -> Root -> Right (Produces sorted order)
void inorder(struct Node* root) {
    if (root != NULL) {
        inorder(root->left);
        printf("%d ", root->data);
        inorder(root->right);
    }
}

// Preorder traversal: Root -> Left -> Right
void preorder(struct Node* root) {
    if (root != NULL) {
        printf("%d ", root->data);
        preorder(root->left);
        preorder(root->right);
    }
}

// Postorder traversal: Left -> Right -> Root
void postorder(struct Node* root) {
    if (root != NULL) {
        postorder(root->left);
        postorder(root->right);
        printf("%d ", root->data);
    }
}

// Free memory of all nodes in BST
void freeTree(struct Node* root) {
    if (root != NULL) {
        freeTree(root->left);
        freeTree(root->right);
        free(root);
    }
}

int main() {
    struct Node* root = NULL;
    printf("=== Binary Search Tree Operations in C ===\n\n");

    // Insert keys
    printf("Inserting keys: 50, 30, 70, 20, 40, 60, 80\n");
    root = insert(root, 50);
    insert(root, 30);
    insert(root, 70);
    insert(root, 20);
    insert(root, 40);
    insert(root, 60);
    insert(root, 80);

    // Tree traversals
    printf("\nInorder Traversal (Sorted order): ");
    inorder(root);
    printf("\n");

    printf("Preorder Traversal: ");
    preorder(root);
    printf("\n");

    printf("Postorder Traversal: ");
    postorder(root);
    printf("\n");

    // Search operations
    int keysToSearch[] = {40, 95};
    for (int i = 0; i < 2; i++) {
        int k = keysToSearch[i];
        struct Node* found = search(root, k);
        if (found != NULL) {
            printf("\nKey %d is present in the BST.", k);
        } else {
            printf("\nKey %d is NOT present in the BST.", k);
        }
    }
    printf("\n");

    // Clean up heap allocation
    freeTree(root);
    printf("\nTree memory freed successfully. Exiting...\n");
    return 0;
}
