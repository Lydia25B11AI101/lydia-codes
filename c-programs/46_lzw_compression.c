/*
 * Title: Lempel-Ziv-Welch (LZW) Data Compression Demonstration
 * Author: Lydia S. Makiwa
 * Date: June 06, 2026
 *
 * Description:
 * This program demonstrates a simplified LZW (Lempel-Ziv-Welch) compression 
 * algorithm in C. It shows how the dictionary-based compression works by building
 * dictionary patterns dynamically during input reading.
 * 
 * Teaches: Structs, string lookup, and foundational compression math.
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define DICT_SIZE 512
#define MAX_STR_LEN 50

typedef struct {
    int code;
    char str[MAX_STR_LEN];
} DictEntry;

DictEntry dictionary[DICT_SIZE];
int dict_count = 0;

void init_dictionary() {
    dict_count = 0;
    // Initialize standard single character ASCII codes (0 to 127)
    for (int i = 0; i < 128; i++) {
        dictionary[dict_count].code = i;
        dictionary[dict_count].str[0] = (char)i;
        dictionary[dict_count].str[1] = '\0';
        dict_count++;
    }
}

int search_dictionary(char *str) {
    for (int i = 0; i < dict_count; i++) {
        if (strcmp(dictionary[i].str, str) == 0) {
            return dictionary[i].code;
        }
    }
    return -1;
}

void add_to_dictionary(char *str) {
    if (dict_count < DICT_SIZE) {
        dictionary[dict_count].code = dict_count;
        strcpy(dictionary[dict_count].str, str);
        dict_count++;
    }
}

void compress_lzw(char *input) {
    printf("Compressing text: \"%s\"\n", input);
    printf("Output LZW Codes: ");
    
    char p[MAX_STR_LEN] = "";
    char c[2] = "";
    char pc[MAX_STR_LEN] = "";
    
    p[0] = input[0];
    p[1] = '\0';
    
    int len = strlen(input);
    for (int i = 1; i < len; i++) {
        c[0] = input[i];
        c[1] = '\0';
        
        strcpy(pc, p);
        strcat(pc, c);
        
        if (search_dictionary(pc) != -1) {
            strcpy(p, pc);
        } else {
            printf("%d ", search_dictionary(p));
            add_to_dictionary(pc);
            strcpy(p, c);
        }
    }
    printf("%d\n", search_dictionary(p));
    printf("Dictionary expanded to %d entries.\n", dict_count);
}

int main() {
    printf("=== LZW Compression Demo ===\n");
    init_dictionary();
    
    char text[] = "TOBEORNOTTOBEORTOBEORNOT";
    compress_lzw(text);
    
    return 0;
}
