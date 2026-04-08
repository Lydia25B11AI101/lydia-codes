# Data Structure 6: Merge Sort
# Author: Lydia S. Makiwa
# Description: Divide-and-conquer sorting — O(n log n) time complexity

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid   = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Demo
import random
data = random.sample(range(1, 100), 12)
print(f"Original:  {data}")
sorted_data = merge_sort(data)
print(f"Sorted:    {sorted_data}")

# Compare with built-in
print(f"Correct:   {sorted_data == sorted(data)} ✅")
print(f"Time Complexity: O(n log n) | Space: O(n)")
