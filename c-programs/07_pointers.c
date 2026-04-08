/* C Program 7: Understanding Pointers
   Author: Lydia S. Makiwa
   Description: Demonstrates pointer basics — address, dereferencing, and swap */

#include <stdio.h>

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main() {
    int x = 42, y = 99;

    printf("=== Pointer Basics ===\n");
    printf("Value of x     : %d\n", x);
    printf("Address of x   : %p\n", (void*)&x);

    int *ptr = &x;
    printf("Pointer ptr    : %p\n", (void*)ptr);
    printf("Value via *ptr : %d\n", *ptr);

    *ptr = 100;
    printf("After *ptr=100 : x = %d\n\n", x);

    printf("=== Swap using Pointers ===\n");
    printf("Before: x = %d, y = %d\n", x, y);
    swap(&x, &y);
    printf("After:  x = %d, y = %d\n", x, y);

    return 0;
}
