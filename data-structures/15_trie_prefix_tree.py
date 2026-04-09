# ============================================================
# Program Title : Trie (Prefix Tree) Data Structure
# Author        : Lydia S. Makiwa
# Date          : 2026-04-09
# Description   : Implements a Trie for fast string insert,
#                 search, and autocomplete. Used in search
#                 engines, spell checkers, and keyboards.
# ============================================================

class TrieNode:
    def __init__(self):
        self.children    = {}   # char -> TrieNode
        self.is_end_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """Insert a word into the trie."""
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_word = True

    def search(self, word):
        """Return True if word exists in the trie."""
        node = self._find_prefix_node(word)
        return node is not None and node.is_end_word

    def starts_with(self, prefix):
        """Return True if any word starts with prefix."""
        return self._find_prefix_node(prefix) is not None

    def autocomplete(self, prefix):
        """Return all words that start with the given prefix."""
        node = self._find_prefix_node(prefix)
        if not node:
            return []
        results = []
        self._dfs(node, prefix.lower(), results)
        return sorted(results)

    def _find_prefix_node(self, prefix):
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _dfs(self, node, current_word, results):
        if node.is_end_word:
            results.append(current_word)
        for char, child in node.children.items():
            self._dfs(child, current_word + char, results)

# -- Demo --------------------------------------------------
if __name__ == "__main__":
    trie = Trie()

    # Build dictionary
    words = [
        "apple", "app", "application", "apply", "apt",
        "banana", "band", "bandana", "banner",
        "python", "pytorch", "pi", "pie",
        "data", "database", "date", "datum",
        "machine", "math", "matrix",
    ]

    for w in words:
        trie.insert(w)

    print("Trie Demo")
    print("=" * 45)

    # Search
    test_words = ["app", "apply", "apt", "application", "apex"]
    print("\nSearch:")
    for w in test_words:
        found = "FOUND" if trie.search(w) else "not found"
        print(f"  search('{w}') -> {found}")

    # Autocomplete
    print("\nAutocomplete:")
    prefixes = ["app", "ban", "py", "dat", "ma"]
    for p in prefixes:
        suggestions = trie.autocomplete(p)
        print(f"  '{p}' -> {suggestions}")

    # Prefix check
    print("\nPrefix check:")
    print(f"  starts_with('ban') -> {trie.starts_with('ban')}")
    print(f"  starts_with('xyz') -> {trie.starts_with('xyz')}")
