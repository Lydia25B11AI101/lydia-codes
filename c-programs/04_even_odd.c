/* C Program 4: Check Even or Odd
   Author: Lydia S. Makiwa */

#include <stdio.h>

int main() {
    int num;
    printf("Enter a number: ");
    scanf("%d", &num);

    if (num % 2 == 0)
        printf("%d is EVEN\n", num);
    else
        printf("%d is ODD\n", num);

    return 0;
}
