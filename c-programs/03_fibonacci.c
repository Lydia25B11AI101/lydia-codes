/* C Program 3: Fibonacci Series
   Author: Lydia S. Makiwa */

#include <stdio.h>

int main() {
    int n, a = 0, b = 1, next;
    printf("How many terms? ");
    scanf("%d", &n);
    printf("Fibonacci Series: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", a);
        next = a + b;
        a = b;
        b = next;
    }
    printf("\n");
    return 0;
}
