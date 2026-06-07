"""
Program: Dynamic Segment Tree with Lazy Propagation
Author: Lydia S. Makiwa
Date: June 7, 2026
Category: Advanced Data Structures / Python Basics

Description:
A Segment Tree is a binary tree used to solve range queries and updates efficiently.
This program implements Range Sum Queries and Range Add Updates using Lazy Propagation.
Lazy propagation defers updates to descendants until necessary, allowing both query 
and update operations to run in O(log N) time.
"""

class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        # Allocate segment tree nodes and lazy values
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self.build(arr, 0, 0, self.n - 1)

    def build(self, arr, node, start, end):
        if start == end:
            self.tree[node] = arr[start]
            return
        mid = (start + end) // 2
        self.build(arr, 2 * node + 1, start, mid)
        self.build(arr, 2 * node + 2, mid + 1, end)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def update_range(self, l, r, val):
        """Increments all elements in range [l, r] by val"""
        self._update_range_internal(0, 0, self.n - 1, l, r, val)

    def _update_range_internal(self, node, start, end, l, r, val):
        # Resolve any pending lazy updates
        if self.lazy[node] != 0:
            self.tree[node] += (end - start + 1) * self.lazy[node]
            if start != end:  # Mark children as lazy
                self.lazy[2 * node + 1] += self.lazy[node]
                self.lazy[2 * node + 2] += self.lazy[node]
            self.lazy[node] = 0

        # No overlap condition
        if start > end or start > r or end < l:
            return

        # Complete overlap condition
        if start >= l and end <= r:
            self.tree[node] += (end - start + 1) * val
            if start != end:
                self.lazy[2 * node + 1] += val
                self.lazy[2 * node + 2] += val
            return

        # Partial overlap condition
        mid = (start + end) // 2
        self._update_range_internal(2 * node + 1, start, mid, l, r, val)
        self._update_range_internal(2 * node + 2, mid + 1, end, l, r, val)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def query_range(self, l, r):
        """Queries the range sum in range [l, r]"""
        return self._query_range_internal(0, 0, self.n - 1, l, r)

    def _query_range_internal(self, node, start, end, l, r):
        # Resolve pending updates
        if self.lazy[node] != 0:
            self.tree[node] += (end - start + 1) * self.lazy[node]
            if start != end:
                self.lazy[2 * node + 1] += self.lazy[node]
                self.lazy[2 * node + 2] += self.lazy[node]
            self.lazy[node] = 0

        # No overlap
        if start > end or start > r or end < l:
            return 0

        # Complete overlap
        if start >= l and end <= r:
            return self.tree[node]

        # Partial overlap
        mid = (start + end) // 2
        sum_left = self._query_range_internal(2 * node + 1, start, mid, l, r)
        sum_right = self._query_range_internal(2 * node + 2, mid + 1, end, l, r)
        return sum_left + sum_right


# Demo / Working Example
if __name__ == "__main__":
    print("=== Segment Tree with Lazy Propagation Demo ===")
    
    arr = [1, 3, 5, 7, 9, 11]
    print(f"Original Array: {arr}")
    
    seg_tree = SegmentTree(arr)
    
    print("\nInitial queries:")
    print(f" -> Sum of range [1, 3] (elements 3, 5, 7): {seg_tree.query_range(1, 3)}") # Expected: 15
    print(f" -> Sum of range [0, 5] (all elements): {seg_tree.query_range(0, 5)}") # Expected: 36

    # Perform a range update: Add 10 to all elements from index 1 to 4
    # Array should become: [1, 13, 15, 17, 19, 11]
    print("\nExecuting range update: Adding 10 to indices [1, 4]...")
    seg_tree.update_range(1, 4, 10)

    print("\nPost-update queries:")
    print(f" -> Sum of range [1, 3] (elements 13, 15, 17): {seg_tree.query_range(1, 3)}") # Expected: 45
    print(f" -> Sum of range [0, 5] (all elements): {seg_tree.query_range(0, 5)}") # Expected: 76
