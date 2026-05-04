/* ============================================================
 * Program Title : Circular Queue using Array
 * Author        : Lydia S. Makiwa
 * Date          : 2026-05-04
 * Description   : Implement a circular queue with enqueue,
 *                 dequeue, peek, and display operations.
 * ============================================================ */

#include <stdio.h>
#define MAX 6

int queue[MAX], front=-1, rear=-1;

int isFull()  { return (rear+1)%MAX == front; }
int isEmpty() { return front == -1; }

void enqueue(int val) {
    if (isFull()) { printf("Queue full!\n"); return; }
    if (isEmpty()) front = rear = 0;
    else rear = (rear+1)%MAX;
    queue[rear] = val;
    printf("Enqueued: %d\n", val);
}

int dequeue() {
    if (isEmpty()) { printf("Queue empty!\n"); return -1; }
    int v = queue[front];
    if (front==rear) front=rear=-1;
    else front = (front+1)%MAX;
    return v;
}

void display() {
    if (isEmpty()) { printf("Queue empty\n"); return; }
    printf("Queue: ");
    int i = front;
    while (1) { printf("%d ",queue[i]); if(i==rear) break; i=(i+1)%MAX; }
    printf("\n");
}

int main() {
    enqueue(10); enqueue(20); enqueue(30); enqueue(40); enqueue(50);
    display();
    printf("Dequeued: %d\n", dequeue());
    printf("Dequeued: %d\n", dequeue());
    enqueue(60); enqueue(70);
    display();
    printf("Circular queue demo complete!\n");
    return 0;
}
