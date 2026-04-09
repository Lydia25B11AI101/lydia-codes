/*
 * Program Title : Stack Implementation using Array
 * Author        : Lydia S. Makiwa
 * Date          : 2026-04-09
 * Description   : Implements a stack (LIFO) with push, pop,
 *                 peek, and overflow/underflow checks.
 *                 Covers: arrays, struct, preprocessor macros.
 */

#include <stdio.h>
#include <stdlib.h>

#define MAX 10

typedef struct {
    int items[MAX];
    int top;
} Stack;

/* Initialise the stack */
void init(Stack* s) { s->top = -1; }

/* Check if stack is full */
int is_full(Stack* s)  { return s->top == MAX - 1; }

/* Check if stack is empty */
int is_empty(Stack* s) { return s->top == -1; }

/* Push element */
void push(Stack* s, int val) {
    if (is_full(s)) { printf("Stack overflow! Cannot push %d\n", val); return; }
    s->items[++(s->top)] = val;
    printf("Pushed %d\n", val);
}

/* Pop element */
int pop(Stack* s) {
    if (is_empty(s)) { printf("Stack underflow!\n"); return -1; }
    return s->items[(s->top)--];
}

/* Peek at top */
int peek(Stack* s) {
    if (is_empty(s)) { printf("Stack is empty.\n"); return -1; }
    return s->items[s->top];
}

/* Display all elements */
void display(Stack* s) {
    if (is_empty(s)) { printf("Stack: [empty]\n"); return; }
    printf("Stack (top -> bottom): ");
    for (int i = s->top; i >= 0; i--) printf("%d ", s->items[i]);
    printf("\n");
}

/* Use case: check balanced parentheses using a stack */
int balanced(char* expr) {
    Stack s;
    init(&s);
    for (int i = 0; expr[i] != '\0'; i++) {
        if (expr[i] == '(' || expr[i] == '[' || expr[i] == '{')
            push(&s, expr[i]);
        else if (expr[i] == ')' || expr[i] == ']' || expr[i] == '}') {
            if (is_empty(&s)) return 0;
            pop(&s);
        }
    }
    return is_empty(&s);
}

int main() {
    Stack s;
    init(&s);

    printf("=== Stack Demo ===\n");
    push(&s, 5); push(&s, 10); push(&s, 15); push(&s, 20);
    display(&s);
    printf("Peek: %d\n", peek(&s));
    printf("Pop:  %d\n", pop(&s));
    printf("Pop:  %d\n", pop(&s));
    display(&s);

    printf("\n=== Balanced Parentheses ===\n");
    char* tests[] = {"(a + b) * [c - d]", "({[hello]})", "(unclosed[", "{mis}matched)"};
    for (int i = 0; i < 4; i++) {
        printf("  %s  -> %s\n", tests[i], balanced(tests[i]) ? "Balanced" : "NOT balanced");
    }
    return 0;
}
