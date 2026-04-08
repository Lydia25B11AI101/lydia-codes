/* C Program 13: Pattern Printing
   Author: Lydia S. Makiwa
   Description: Prints various number and star patterns using loops */

#include <stdio.h>

void right_triangle(int n) {
    printf("Right Triangle (n=%d):\n", n);
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) printf("* ");
        printf("\n");
    }
}

void pyramid(int n) {
    printf("\nPyramid (n=%d):\n", n);
    for (int i = 1; i <= n; i++) {
        for (int j = i; j < n; j++) printf("  ");
        for (int j = 1; j <= (2*i - 1); j++) printf("* ");
        printf("\n");
    }
}

void number_pattern(int n) {
    printf("\nNumber Pattern (n=%d):\n", n);
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) printf("%d ", j);
        printf("\n");
    }
}

void diamond(int n) {
    printf("\nDiamond (n=%d):\n", n);
    for (int i = 1; i <= n; i++) {
        for (int j = i; j < n; j++) printf(" ");
        for (int j = 1; j <= (2*i-1); j++) printf("*");
        printf("\n");
    }
    for (int i = n-1; i >= 1; i--) {
        for (int j = n; j > i; j--) printf(" ");
        for (int j = 1; j <= (2*i-1); j++) printf("*");
        printf("\n");
    }
}

int main() {
    right_triangle(5);
    pyramid(5);
    number_pattern(5);
    diamond(5);
    return 0;
}
