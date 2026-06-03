# ==============================================================================
# Title: Bloom Filter from Scratch in Python
# Author: Lydia S. Makiwa
# Date: June 3, 2026
# Description: Implements a memory-efficient probabilistic data structure (Bloom Filter)
#              using an integer as an arbitrary-precision bit vector and custom polynomial
#              hash functions. Explores space-vs-accuracy trade-offs in big data.
# ==============================================================================

class BloomFilter:
    def __init__(self, size=1000, num_hashes=3):
        """
        size: total number of bits in the bit vector.
        num_hashes: number of hash functions to generate per item.
        """
        self.size = size
        self.num_hashes = num_hashes
        # Python handles arbitrary precision integers, so we can use a single large int as our bit array
        self.bit_vector = 0 

    def _hashes(self, item):
        """
        Generates custom polynomial hashes (similar to MurmurHash/DJB2 logic) for an item.
        Produces list of length self.num_hashes containing bit indices.
        """
        indices = []
        # Convert item to string to hash uniformly
        item_str = str(item)
        
        # We can simulate different hash functions using distinct seed values
        for i in range(self.num_hashes):
            hash_val = 5381 + i
            for char in item_str:
                # Polynomial hash: (hash * 33) + ASCII of char
                hash_val = ((hash_val << 5) + hash_val) + ord(char)
            indices.append(hash_val % self.size)
            
        return indices

    def add(self, item):
        """Inserts an item into the bloom filter by setting corresponding bits to 1."""
        indices = self._hashes(item)
        for index in indices:
            # Set the bit at 'index' to 1
            self.bit_vector |= (1 << index)

    def contains(self, item):
        """
        Checks if an item is possibly in the bloom filter.
        Returns False if definitely NOT in the filter.
        Returns True if possibly in the filter (with chance of false positive).
        """
        indices = self._hashes(item)
        for index in indices:
            # Check if the bit at 'index' is 0
            if not (self.bit_vector & (1 << index)):
                return False # Definitely not present
        return True # Possibly present (all bits were set to 1)

# --- Demo & Example ---
if __name__ == "__main__":
    print("--- Probabilistic Data Structures: Bloom Filter Demo ---")
    
    # Instantiate Bloom Filter with size of 50 bits and 3 hashes
    bf = BloomFilter(size=50, num_hashes=3)
    
    # Add words
    words_to_add = ["apple", "banana", "cherry", "grape", "orange"]
    print(f"\nAdding items to Bloom Filter: {words_to_add}")
    for word in words_to_add:
        bf.add(word)
        
    print(f"Current Bit-Vector representation (binary): {bin(bf.bit_vector)}")
    
    # Test containment (membership)
    test_words = ["apple", "banana", "watermelon", "pineapple", "cherry", "mango"]
    print("\nTesting membership:")
    for word in test_words:
        present = bf.contains(word)
        status = "PRESENT (Possibly)" if present else "ABSENT (Definitely)"
        # Check if it was actually in our added list to determine if it's a false positive
        actual = word in words_to_add
        is_false_positive = present and not actual
        
        print(f"  Is '{word}' in filter? -> {status}", end="")
        if is_false_positive:
            print(" [FALSE POSITIVE DETECTED!]")
        else:
            print(" [Correct]")
