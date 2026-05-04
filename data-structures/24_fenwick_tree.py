# ============================================================
# Program Title : Fenwick Tree (Binary Indexed Tree)
# Author        : Lydia S. Makiwa
# Date          : 2026-05-04
# Description   : Support point updates and prefix sum queries
#                 in O(log n) using a Fenwick tree.
# ============================================================

class FenwickTree:
    def __init__(self, n):
        self.n    = n
        self.tree = [0] * (n + 1)

    def update(self, i, delta):
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)

    def prefix_sum(self, i):
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & (-i)
        return total

    def range_sum(self, l, r):
        return self.prefix_sum(r) - self.prefix_sum(l - 1)

# Demo
arr = [3, 2, -1, 6, 5, 4, -3, 3, 7, 2, 3]
n   = len(arr)
ft  = FenwickTree(n)
for i, v in enumerate(arr, 1):
    ft.update(i, v)

print('Array:', arr)
print('Prefix sum [1..5]:', ft.prefix_sum(5))
print('Range sum  [3..8]:', ft.range_sum(3, 8))

# Update index 3 (+5)
ft.update(3, 5)
print('After updating index 3 by +5:')
print('Range sum  [1..5]:', ft.range_sum(1, 5))
print('Fenwick Tree demo complete!')
