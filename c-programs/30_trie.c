/* Program Title: Trie (Prefix Tree) in C
   Author: Lydia S. Makiwa
   Date: 2026-05-05
   Description: Implements a Trie data structure for efficient
                string insertion, search, and prefix checking.
                Used in autocomplete engines and spell checkers. */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ALPHA 26

typedef struct TrieNode {
    struct TrieNode* children[ALPHA];
    int is_end;
} TrieNode;

TrieNode* new_node() {
    TrieNode* n = (TrieNode*)calloc(1, sizeof(TrieNode));
    n->is_end = 0;
    return n;
}

void insert(TrieNode* root, const char* word) {
    TrieNode* cur = root;
    while (*word) {
        int idx = *word - 'a';
        if (!cur->children[idx])
            cur->children[idx] = new_node();
        cur = cur->children[idx];
        word++;
    }
    cur->is_end = 1;
}

int search(TrieNode* root, const char* word) {
    TrieNode* cur = root;
    while (*word) {
        int idx = *word - 'a';
        if (!cur->children[idx]) return 0;
        cur = cur->children[idx];
        word++;
    }
    return cur->is_end;
}

int starts_with(TrieNode* root, const char* prefix) {
    TrieNode* cur = root;
    while (*prefix) {
        int idx = *prefix - 'a';
        if (!cur->children[idx]) return 0;
        cur = cur->children[idx];
        prefix++;
    }
    return 1;
}

void free_trie(TrieNode* node) {
    for (int i = 0; i < ALPHA; i++)
        if (node->children[i]) free_trie(node->children[i]);
    free(node);
}

int main() {
    TrieNode* root = new_node();
    const char* words[] = {"apple","app","application","apply","apt","banana"};
    int n = 6;

    printf("Inserting words into Trie...\n");
    for (int i = 0; i < n; i++) {
        insert(root, words[i]);
        printf("  Inserted: %s\n", words[i]);
    }

    printf("\nSearch results:\n");
    const char* queries[] = {"apple","ap","application","mango","app"};
    for (int i = 0; i < 5; i++) {
        printf("  search('%s')   = %s\n", queries[i], search(root, queries[i]) ? "FOUND" : "NOT FOUND");
        printf("  prefix('%s')   = %s\n", queries[i], starts_with(root, queries[i]) ? "EXISTS" : "NO PREFIX");
    }

    free_trie(root);
    return 0;
}
