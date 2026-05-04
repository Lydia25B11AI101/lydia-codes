/* ============================================================
 * Program Title : Binary Tree Traversals
 * Author        : Lydia S. Makiwa
 * Date          : 2026-05-04
 * Description   : Build a BST and print inorder, preorder,
 *                 and postorder traversals recursively.
 * ============================================================ */

#include <stdio.h>
#include <stdlib.h>

typedef struct Node { int data; struct Node *left, *right; } Node;

Node* newNode(int d){
    Node *n = malloc(sizeof(Node));
    n->data = d; n->left = n->right = NULL;
    return n;
}

Node* insert(Node *root, int d){
    if (!root) return newNode(d);
    if (d < root->data) root->left  = insert(root->left,  d);
    else                root->right = insert(root->right, d);
    return root;
}

void inorder(Node *r)  { if(r){ inorder(r->left);  printf("%d ",r->data); inorder(r->right);  } }
void preorder(Node *r) { if(r){ printf("%d ",r->data); preorder(r->left);  preorder(r->right); } }
void postorder(Node *r){ if(r){ postorder(r->left); postorder(r->right); printf("%d ",r->data); } }

int main(){
    int vals[] = {50,30,70,20,40,60,80};
    Node *root = NULL;
    for(int i=0;i<7;i++) root=insert(root,vals[i]);
    printf("Inorder   (sorted): "); inorder(root);   printf("\n");
    printf("Preorder           : "); preorder(root);  printf("\n");
    printf("Postorder          : "); postorder(root); printf("\n");
    printf("BST traversals complete!\n");
    return 0;
}
