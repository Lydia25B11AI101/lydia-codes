/* C Program 6: Bubble Sort Algorithm
   Author: Lydia S. Makiwa
   Description: Sorts an array in ascending order using bubble sort */

#include <stdio.h>

void print_array(int arr[], int n) {
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

void bubble_sort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        int swapped = 0;
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                swapped = 1;
            }
        }
        if (!swapped) break; /* Optimised: stop if already sorted */
    }
}

int main() {
    int arr[] = {64, 34, 25, 12, 22, 11, 90, 45, 7, 55};
    int n = sizeof(arr) / sizeof(arr[0]);

    printf("Original array: ");
    print_array(arr, n);

    bubble_sort(arr, n);

    printf("Sorted array:   ");
    print_array(arr, n);

    return 0;
}
