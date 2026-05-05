# Program Title: Suffix Array (String Indexing)
# Author: Lydia S. Makiwa
# Date: 2026-05-05
# Description: Builds a suffix array for fast substring search —
#              the backbone of search engines, DNA sequencing tools,
#              and text compression (BWT / SA-IS).

def build_suffix_array(text):
    """Returns sorted indices of all suffixes of `text`."""
    suffixes = [(text[i:], i) for i in range(len(text))]
    suffixes.sort()
    return [idx for _, idx in suffixes]

def search_pattern(text, sa, pattern):
    """Binary search on suffix array — O(m log n)."""
    lo, hi = 0, len(sa)
    while lo < hi:
        mid = (lo + hi) // 2
        if text[sa[mid]:].startswith(pattern):
            # Scan left and right for all matches
            results = [sa[mid]]
            # expand left
            k = mid - 1
            while k >= 0 and text[sa[k]:].startswith(pattern):
                results.append(sa[k]); k -= 1
            # expand right
            k = mid + 1
            while k < len(sa) and text[sa[k]:].startswith(pattern):
                results.append(sa[k]); k += 1
            return sorted(results)
        elif text[sa[mid]:] < pattern:
            lo = mid + 1
        else:
            hi = mid
    return []

def lcp_array(text, sa):
    """Longest Common Prefix array for adjacent suffixes."""
    n    = len(text)
    rank = [0] * n
    for i, idx in enumerate(sa):
        rank[idx] = i
    lcp  = [0] * n
    h    = 0
    for i in range(n):
        if rank[i] > 0:
            j = sa[rank[i] - 1]
            while i + h < n and j + h < n and text[i+h] == text[j+h]:
                h += 1
            lcp[rank[i]] = h
            if h: h -= 1
    return lcp

# ─── Demo ───
text = "banana"
sa   = build_suffix_array(text)

print(f"Text: {text}")
print("\nSuffix Array:")
for rank, idx in enumerate(sa):
    print(f"  SA[{rank}] = {idx:2d}  suffix = '{text[idx:]}'")

lcp = lcp_array(text, sa)
print("\nLCP Array:", lcp)

print("\nPattern Search:")
for pat in ["an", "ana", "nana", "xyz"]:
    positions = search_pattern(text, sa, pat)
    if positions:
        print(f"  '{pat}' found at positions: {positions}")
    else:
        print(f"  '{pat}' not found.")
