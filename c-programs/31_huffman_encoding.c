/* Program Title: Huffman Encoding (Greedy Compression)
   Author: Lydia S. Makiwa
   Date: 2026-05-05
   Description: Implements Huffman encoding — a lossless data compression
                algorithm using a priority queue (min-heap) and binary tree.
                Core concept in ZIP, PNG, and JPEG compression. */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX 256

typedef struct Node {
    char ch;
    int  freq;
    struct Node *left, *right;
} Node;

typedef struct {
    Node* nodes[MAX];
    int   size;
} MinHeap;

Node* new_node(char ch, int freq) {
    Node* n = malloc(sizeof(Node));
    n->ch = ch; n->freq = freq;
    n->left = n->right = NULL;
    return n;
}

void heap_push(MinHeap* h, Node* n) {
    int i = h->size++;
    h->nodes[i] = n;
    while (i > 0) {
        int p = (i - 1) / 2;
        if (h->nodes[p]->freq > h->nodes[i]->freq) {
            Node* tmp = h->nodes[p];
            h->nodes[p] = h->nodes[i];
            h->nodes[i] = tmp;
            i = p;
        } else break;
    }
}

Node* heap_pop(MinHeap* h) {
    Node* top = h->nodes[0];
    h->nodes[0] = h->nodes[--h->size];
    int i = 0;
    while (1) {
        int l = 2*i+1, r = 2*i+2, smallest = i;
        if (l < h->size && h->nodes[l]->freq < h->nodes[smallest]->freq) smallest = l;
        if (r < h->size && h->nodes[r]->freq < h->nodes[smallest]->freq) smallest = r;
        if (smallest == i) break;
        Node* tmp = h->nodes[i]; h->nodes[i] = h->nodes[smallest]; h->nodes[smallest] = tmp;
        i = smallest;
    }
    return top;
}

void print_codes(Node* root, char* code, int depth) {
    if (!root->left && !root->right) {
        code[depth] = '\0';
        printf("  '%c' (freq %d): %s\n", root->ch, root->freq, depth ? code : "0");
        return;
    }
    if (root->left)  { code[depth]='0'; print_codes(root->left,  code, depth+1); }
    if (root->right) { code[depth]='1'; print_codes(root->right, code, depth+1); }
}

int main() {
    const char* text = "huffman encoding example";
    int freq[128] = {0};
    for (int i = 0; text[i]; i++) freq[(unsigned char)text[i]]++;

    MinHeap h; h.size = 0;
    for (int i = 0; i < 128; i++)
        if (freq[i]) heap_push(&h, new_node((char)i, freq[i]));

    printf("Building Huffman tree for: \"%s\"\n\n", text);

    while (h.size > 1) {
        Node* l = heap_pop(&h);
        Node* r = heap_pop(&h);
        Node* merged = new_node('$', l->freq + r->freq);
        merged->left = l; merged->right = r;
        heap_push(&h, merged);
    }

    printf("Huffman Codes:\n");
    char code[128];
    print_codes(h.nodes[0], code, 0);
    return 0;
}
