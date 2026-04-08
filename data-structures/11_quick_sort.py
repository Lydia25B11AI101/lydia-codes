# Data Structure 11: Quick Sort
# Author: Lydia S. Makiwa
# Description: Partition-based sorting — average O(n log n)

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot  = arr[len(arr) // 2]
    left   = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right  = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

import random
data = random.sample(range(1, 50), 10)
print(f"Original: {data}")
print(f"Sorted:   {quick_sort(data)}")
print("\nSorting Algorithm Comparison:")
print(f"  Bubble Sort : O(n²)     — simple but slow")
print(f"  Selection   : O(n²)     — few swaps")
print(f"  Insertion   : O(n²)     — good for small/nearly sorted")
print(f"  Merge Sort  : O(n logn) — stable, extra space")
print(f"  Quick Sort  : O(n logn) — fast in practice, in-place")
