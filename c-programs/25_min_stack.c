/* ============================================================
   Program Title : Min Stack — O(1) Get-Minimum
   Author        : Lydia S. Makiwa
   Date          : 2026-05-03
   Description   : Stack that retrieves the minimum element in
                   O(1) time using an auxiliary min-stack.
   ============================================================ */

#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#define MAX 100

typedef struct {
    int data[MAX];
    int minData[MAX];
    int top;
} MinStack;

void init(MinStack *s)    { s->top = -1; }
int  isEmpty(MinStack *s) { return s->top == -1; }

void push(MinStack *s, int val) {
    if (s->top >= MAX-1) { printf("Stack overflow!\n"); return; }
    s->top++;
    s->data[s->top] = val;
    if (s->top == 0)
        s->minData[s->top] = val;
    else
        s->minData[s->top] = (val < s->minData[s->top-1]) ? val : s->minData[s->top-1];
}

int pop(MinStack *s) {
    if (isEmpty(s)) { printf("Stack underflow!\n"); return INT_MIN; }
    return s->data[s->top--];
}

int getMin(MinStack *s) {
    if (isEmpty(s)) { printf("Stack is empty!\n"); return INT_MIN; }
    return s->minData[s->top];
}

int peek(MinStack *s) {
    if (isEmpty(s)) return INT_MIN;
    return s->data[s->top];
}

int main() {
    MinStack s;
    init(&s);

    int vals[] = {5, 3, 8, 2, 7, 1, 4};
    printf("Pushing values and tracking min:\n");
    for (int i = 0; i < 7; i++) {
        push(&s, vals[i]);
        printf("  push(%d) -> min=%d\n", vals[i], getMin(&s));
    }

    printf("\nPopping values:\n");
    while (!isEmpty(&s)) {
        printf("  pop=%d -> min=%d\n", pop(&s),
               isEmpty(&s) ? -1 : getMin(&s));
    }
    return 0;
}
