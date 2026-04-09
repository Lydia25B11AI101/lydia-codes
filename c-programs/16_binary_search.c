/* C Program 16: Binary Search
   Author: Lydia S. Makiwa
   Description: Iterative and recursive binary search in C */

#include <stdio.h>

int binary_search_iter(int arr[], int n, int target) {
    int left = 0, right = n - 1;
    while (left <= right) {
        int mid = (left + right) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target)  left  = mid + 1;
        else                    right = mid - 1;
    }
    return -1;
}

int binary_search_rec(int arr[], int left, int right, int target) {
    if (left > right) return -1;
    int mid = (left + right) / 2;
    if (arr[mid] == target) return mid;
    if (arr[mid] < target)  return binary_search_rec(arr, mid+1, right, target);
    return binary_search_rec(arr, left, mid-1, target);
}

int main() {
    int arr[] = {2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91};
    int n = sizeof(arr) / sizeof(arr[0]);

    printf("Array: ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n\n");

    int targets[] = {23, 72, 100, 2};
    for (int i = 0; i < 4; i++) {
        int t   = targets[i];
        int idx = binary_search_iter(arr, n, t);
        if (idx != -1)
            printf("Found %3d at index %d (iterative)\n", t, idx);
        else
            printf("%3d not found (iterative)\n", t);

        idx = binary_search_rec(arr, 0, n-1, t);
        if (idx != -1)
            printf("Found %3d at index %d (recursive)\n\n", t, idx);
        else
            printf("%3d not found (recursive)\n\n", t);
    }
    return 0;
}
