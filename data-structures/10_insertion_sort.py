# Data Structure 10: Insertion Sort
# Author: Lydia S. Makiwa
# Description: Builds a sorted list one element at a time

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key  = arr[i]
        j    = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        print(f"  Pass {i}: {arr}")
    return arr

data = [12, 11, 13, 5, 6, 9, 3]
print(f"Original: {data}\n")
result = insertion_sort(data.copy())
print(f"\nSorted:   {result}")
print("Best Case: O(n) | Worst Case: O(n²) | Space: O(1)")
