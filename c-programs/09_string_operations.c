/* C Program 9: String Operations
   Author: Lydia S. Makiwa
   Description: Common string operations without using string.h heavily */

#include <stdio.h>
#include <string.h>
#include <ctype.h>

void reverse_string(char str[], char result[]) {
    int len = strlen(str);
    for (int i = 0; i < len; i++)
        result[i] = str[len - 1 - i];
    result[len] = '\0';
}

int is_palindrome(char str[]) {
    int len = strlen(str);
    for (int i = 0; i < len / 2; i++)
        if (tolower(str[i]) != tolower(str[len - 1 - i])) return 0;
    return 1;
}

void to_uppercase(char str[]) {
    for (int i = 0; str[i]; i++) str[i] = toupper(str[i]);
}

int count_vowels(char str[]) {
    int count = 0;
    for (int i = 0; str[i]; i++) {
        char c = tolower(str[i]);
        if (c=='a'||c=='e'||c=='i'||c=='o'||c=='u') count++;
    }
    return count;
}

int main() {
    char str[] = "Lydia Makiwa";
    char rev[50];

    printf("Original  : %s\n", str);
    reverse_string(str, rev);
    printf("Reversed  : %s\n", rev);
    printf("Palindrome: %s\n", is_palindrome(str) ? "Yes" : "No");
    printf("Vowels    : %d\n", count_vowels(str));
    printf("Length    : %lu\n", strlen(str));

    to_uppercase(str);
    printf("Uppercase : %s\n", str);

    printf("\nPalindrome test: \'racecar' → %s\n",
           is_palindrome("racecar") ? "Yes ✓" : "No ✗");

    return 0;
}
