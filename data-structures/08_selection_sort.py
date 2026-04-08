# Data Structure 8: Selection Sort
# Author: Lydia S. Makiwa
# Description: Selection sort — finds minimum element and places it in order

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        print(f"  Pass {i+1}: {arr}")
    return arr

data = [64, 25, 12, 22, 11, 90, 45]
print(f"Original: {data}\n")
result = selection_sort(data.copy())
print(f"\nSorted:   {result}")
print("Time Complexity: O(n²) | Space: O(1)")
