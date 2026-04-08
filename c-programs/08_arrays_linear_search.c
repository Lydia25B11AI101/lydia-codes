/* C Program 8: Arrays and Linear Search
   Author: Lydia S. Makiwa
   Description: Demonstrates array operations and linear search */

#include <stdio.h>

int linear_search(int arr[], int n, int target) {
    for (int i = 0; i < n; i++)
        if (arr[i] == target) return i;
    return -1;
}

int find_max(int arr[], int n) {
    int max = arr[0];
    for (int i = 1; i < n; i++)
        if (arr[i] > max) max = arr[i];
    return max;
}

int find_min(int arr[], int n) {
    int min = arr[0];
    for (int i = 1; i < n; i++)
        if (arr[i] < min) min = arr[i];
    return min;
}

double find_avg(int arr[], int n) {
    int sum = 0;
    for (int i = 0; i < n; i++) sum += arr[i];
    return (double)sum / n;
}

int main() {
    int arr[] = {23, 7, 45, 12, 67, 3, 89, 34, 56, 19};
    int n = sizeof(arr) / sizeof(arr[0]);

    printf("Array: ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]);

    printf("\n\nMax: %d", find_max(arr, n));
    printf("\nMin: %d", find_min(arr, n));
    printf("\nAvg: %.2f", find_avg(arr, n));

    int target = 67;
    int idx = linear_search(arr, n, target);
    if (idx != -1)
        printf("\n\nLinear Search: %d found at index %d\n", target, idx);
    else
        printf("\n\nLinear Search: %d not found\n", target);

    return 0;
}
