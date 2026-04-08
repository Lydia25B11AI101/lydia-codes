# Python Program 13: Binary Search Algorithm
# Author: Lydia S. Makiwa
# Description: Implements iterative and recursive binary search

def binary_search_iterative(arr, target):
    """Binary search — O(log n) time complexity."""
    left, right = 0, len(arr) - 1
    steps = 0
    while left <= right:
        steps += 1
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid, steps
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1, steps

def binary_search_recursive(arr, target, left=0, right=None):
    """Recursive binary search."""
    if right is None: right = len(arr) - 1
    if left > right: return -1
    mid = (left + right) // 2
    if arr[mid] == target: return mid
    elif arr[mid] < target: return binary_search_recursive(arr, target, mid+1, right)
    else: return binary_search_recursive(arr, target, left, mid-1)

# Demo
sorted_list = list(range(0, 100, 5))  # [0, 5, 10, ..., 95]
print(f"Array: {sorted_list}\n")

targets = [35, 70, 42, 0, 95]
print(f"{'Target':>8} {'Index':>8} {'Steps':>8} {'Found?':>8}")
print("-" * 40)
for t in targets:
    idx, steps = binary_search_iterative(sorted_list, t)
    found = f"✅ @ index {idx}" if idx != -1 else "❌ Not found"
    print(f"{t:>8} {str(idx):>8} {steps:>8}     {found}")
