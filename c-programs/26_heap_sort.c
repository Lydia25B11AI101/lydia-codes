/* ============================================================
 * Program Title : Heap Sort
 * Author        : Lydia S. Makiwa
 * Date          : 2026-05-04
 * Description   : Implement heap sort using a max-heap.
 *                 Time: O(n log n), Space: O(1).
 * ============================================================ */

#include <stdio.h>

void swap(int *a, int *b) { int t=*a; *a=*b; *b=t; }

void heapify(int arr[], int n, int i) {
    int largest = i;
    int left    = 2*i + 1;
    int right   = 2*i + 2;
    if (left < n  && arr[left]  > arr[largest]) largest = left;
    if (right < n && arr[right] > arr[largest]) largest = right;
    if (largest != i) {
        swap(&arr[i], &arr[largest]);
        heapify(arr, n, largest);
    }
}

void heapSort(int arr[], int n) {
    /* Build max heap */
    for (int i = n/2 - 1; i >= 0; i--)
        heapify(arr, n, i);
    /* Extract elements one by one */
    for (int i = n-1; i > 0; i--) {
        swap(&arr[0], &arr[i]);
        heapify(arr, i, 0);
    }
}

int main() {
    int arr[] = {12, 11, 13, 5, 6, 7, 3, 1, 9};
    int n = sizeof(arr)/sizeof(arr[0]);
    printf("Before: ");
    for (int i=0;i<n;i++) printf("%d ",arr[i]);
    heapSort(arr, n);
    printf("\nAfter : ");
    for (int i=0;i<n;i++) printf("%d ",arr[i]);
    printf("\nHeap sort complete!\n");
    return 0;
}
