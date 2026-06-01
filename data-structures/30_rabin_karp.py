"""
Program  : 30_rabin_karp.py
Title    : Rabin-Karp String Matching Algorithm
Author   : Lydia S. Makiwa
Date     : 2026-06-01

Description:
    Implements the Rabin-Karp string matching algorithm using
    rolling hash (Rabin fingerprint). Efficiently finds all
    occurrences of a pattern in a text in O(n+m) average time.
    Used in plagiarism detection, DNA sequence matching, and
    search engines like grep and Ctrl+F.
"""


def rabin_karp_search(text, pattern, prime=101):
    """
    Find all occurrences of pattern in text using Rabin-Karp.
    
    Uses a rolling hash function to compare substrings without
    re-hashing from scratch each time.
    
    Args:
        text: The text to search in
        pattern: The pattern to find
        prime: A prime number for the hash modulus
    
    Returns:
        list of starting indices where pattern is found
    """
    n, m = len(text), len(pattern)
    if m == 0 or m > n:
        return []
    
    base = 256  # Number of characters in ASCII
    matches = []
    
    # Calculate hash for pattern and first window of text
    pattern_hash = 0
    window_hash = 0
    
    # Calculate base^(m-1) mod prime for rolling hash
    h = 1
    for _ in range(m - 1):
        h = (h * base) % prime
    
    # Compute hash values for pattern and first window
    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % prime
        window_hash = (base * window_hash + ord(text[i])) % prime
    
    # Slide the window over the text
    for i in range(n - m + 1):
        # If hashes match, verify character by character
        if pattern_hash == window_hash:
            # Check characters (could be a hash collision)
            j = 0
            while j < m and text[i + j] == pattern[j]:
                j += 1
            if j == m:
                matches.append(i)
        
        # Calculate hash for next window using rolling hash
        if i < n - m:
            # Remove leading character's contribution
            window_hash = (base * (window_hash - ord(text[i]) * h) 
                           + ord(text[i + m])) % prime
            
            # Handle negative hash
            if window_hash < 0:
                window_hash += prime
    
    return matches


def highlight_matches(text, matches, pattern_length):
    """Return strings with matches highlighted using brackets."""
    results = []
    prev_end = 0
    
    for start in sorted(matches):
        # Add text before this match
        if start > prev_end:
            results.append(text[prev_end:start])
        # Highlight the match
        results.append(f"[{text[start:start + pattern_length]}]")
        prev_end = start + pattern_length
    
    # Add remaining text
    if prev_end < len(text):
        results.append(text[prev_end:])
    
    return "".join(results)


def rabin_karp_2d(grid, pattern):
    """
    Search for a 2D pattern in a 2D grid.
    Useful for image pattern matching and game boards.
    """
    grid_rows, grid_cols = len(grid), len(grid[0])
    p_rows, p_cols = len(pattern), len(pattern[0])
    
    positions = []
    
    for r in range(grid_rows - p_rows + 1):
        for c in range(grid_cols - p_cols + 1):
            match = True
            for pr in range(p_rows):
                for pc in range(p_cols):
                    if grid[r + pr][c + pc] != pattern[pr][pc]:
                        match = False
                        break
                if not match:
                    break
            if match:
                positions.append((r, c))
    
    return positions


# ===== DEMO =====
if __name__ == "__main__":
    print("=" * 55)
    print("   RABIN-KARP STRING MATCHING")
    print("=" * 55)
    
    # Demo 1: Basic string search
    print("\n📝 Demo 1: Basic string search")
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    
    print(f"   Text:    {text}")
    print(f"   Pattern: {pattern}")
    
    matches = rabin_karp_search(text, pattern)
    print(f"   Pattern found at indices: {matches}")
    print(f"   Highlighted: {highlight_matches(text, matches, len(pattern))}")
    
    # Demo 2: Multiple occurrences
    print("\n📝 Demo 2: Multiple occurrences")
    text = "AABAACAADAABAABA"
    pattern = "AABA"
    
    matches = rabin_karp_search(text, pattern)
    print(f"   Text:    {text}")
    print(f"   Pattern: {pattern}")
    print(f"   Found at: {matches}")
    print(f"   Highlighted: {highlight_matches(text, matches, len(pattern))}")
    
    # Demo 3: No match
    print("\n📝 Demo 3: Pattern not found")
    text = "The quick brown fox"
    pattern = "cat"
    matches = rabin_karp_search(text, pattern)
    print(f"   Text:    {text}")
    print(f"   Pattern: {pattern}")
    print(f"   Found at: {matches}")
    
    # Demo 4: Hash collision handling
    print("\n📝 Demo 4: DNA sequence search")
    dna = "ATCGTACGATCGTAGCTAGCTAGCTGATCGTAGC"
    codon = "ATC"  # Common start codon
    
    matches = rabin_karp_search(dna, codon)
    print(f"   DNA sequence: {dna}")
    print(f"   Codon '{codon}' found at: {matches}")
    print(f"   Highlighted: {highlight_matches(dna, matches, len(codon))}")
    
    # Demo 5: 2D pattern matching
    print("\n📝 Demo 5: 2D grid pattern matching")
    grid = [
        "ABAB",
        "BABA",
        "ABAB",
        "BABA"
    ]
    pattern_2d = [
        "AB",
        "BA"
    ]
    
    positions = rabin_karp_2d(grid, pattern_2d)
    print("   2D Grid:")
    for row in grid:
        print(f"     {row}")
    print("   Pattern:")
    for row in pattern_2d:
        print(f"     {row}")
    print(f"   Pattern found at positions: {positions}")
    
    print("\n💡 Rabin-Karp is used in: plagiarism detectors,")
    print("   DNA sequence alignment, and intrusion detection systems!")
