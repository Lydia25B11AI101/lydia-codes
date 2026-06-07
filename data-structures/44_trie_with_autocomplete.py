"""
Program: Trie (Prefix Tree) with Autocomplete and Frequency Tracking
Author: Lydia S. Makiwa
Date: June 7, 2026
Category: Data Structures / Python Basics

Description:
A Trie (Prefix Tree) is a specialized tree-like data structure used to store 
associative arrays where the keys are usually strings. This advanced program 
extends a basic Trie by tracking search frequency and providing sorted top-k 
autocomplete suggestions for queries based on past insertion counts.
"""

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0  # Tracks how many times the word is inserted


class TrieWithAutocomplete:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, frequency=1):
        """Inserts a word into the trie, adding to its frequency score"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.frequency += frequency

    def _dfs_collect(self, node, prefix, results):
        """Helper to recursively traverse and collect all words below a node"""
        if node.is_end_of_word:
            results.append((prefix, node.frequency))
            
        for char, child_node in node.children.items():
            self._dfs_collect(child_node, prefix + char, results)

    def autocomplete(self, prefix, top_k=3):
        """
        Returns top_k autocompleted suggestions that match the given prefix, 
        sorted by frequency of insertion/usage.
        """
        node = self.root
        # Step 1: Navigate to the end of the prefix
        for char in prefix:
            if char not in node.children:
                return []  # Prefix not found
            node = node.children[char]

        # Step 2: Traverse depth-first to collect all candidate words
        candidates = []
        self._dfs_collect(node, prefix, candidates)

        # Step 3: Sort by frequency descending and return top_k words
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[:top_k]


# Demo / Working Example
if __name__ == "__main__":
    print("=== Trie Autocomplete System with Frequency Sorting ===")
    
    trie = TrieWithAutocomplete()

    # Seed the Trie with words and varying usage frequencies
    trie.insert("python", 15)
    trie.insert("pytorch", 25)
    trie.insert("pycharm", 5)
    trie.insert("pyramid", 3)
    trie.insert("pygame", 8)
    trie.insert("data", 30)
    trie.insert("database", 45)
    trie.insert("datatable", 12)

    # Autocomplete test 1
    prefix_1 = "py"
    print(f"\nSearching autocomplete suggestions for prefix: '{prefix_1}'")
    suggestions_1 = trie.autocomplete(prefix_1, top_k=3)
    for index, (word, freq) in enumerate(suggestions_1, 1):
        print(f" {index}. {word} (Frequency/Score: {freq})")

    # Autocomplete test 2
    prefix_2 = "data"
    print(f"\nSearching autocomplete suggestions for prefix: '{prefix_2}'")
    suggestions_2 = trie.autocomplete(prefix_2, top_k=2)
    for index, (word, freq) in enumerate(suggestions_2, 1):
        print(f" {index}. {word} (Frequency/Score: {freq})")

    # Autocomplete test with non-existent prefix
    prefix_3 = "xyz"
    print(f"\nSearching autocomplete suggestions for prefix: '{prefix_3}'")
    print(" Suggestions found:", trie.autocomplete(prefix_3))
