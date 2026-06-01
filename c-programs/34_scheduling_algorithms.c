/*
 * Program  : 34_scheduling_algorithms.c
 * Title    : CPU Scheduling Algorithms (FCFS, SJF, RR, Priority)
 * Author   : Lydia S. Makiwa
 * Date     : 2026-06-01
 *
 * Description:
 *   Implements four classic CPU scheduling algorithms used in
 *   operating systems: First-Come-First-Serve, Shortest Job First,
 *   Round Robin, and Priority Scheduling. Calculates waiting time,
 *   turnaround time, and CPU utilisation. Essential knowledge for
 *   systems programming and OS internships.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define MAX_PROCESSES 10

/* Structure to represent a process */
typedef struct {
    int pid;            /* Process ID */
    int arrival_time;   /* When process arrives */
    int burst_time;     /* CPU time needed */
    int priority;       /* Priority (lower = higher) */
    int remaining_time; /* For preemptive algorithms */
    int completion_time;
    int turnaround_time;
    int waiting_time;
    int started;        /* Flag: has execution started? */
} Process;

/* ---------- First-Come-First-Serve Scheduling ---------- */
void fcfs_schedule(Process processes[], int n) {
    printf("\n--- FCFS (First-Come-First-Serve) Scheduling ---\n");
    
    /* Sort by arrival time (FCFS) */
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (processes[j].arrival_time > processes[j + 1].arrival_time) {
                Process temp = processes[j];
                processes[j] = processes[j + 1];
                processes[j + 1] = temp;
            }
        }
    }
    
    int current_time = 0;
    float total_wait = 0, total_turnaround = 0;
    
    printf("PID\tArrival\tBurst\tStart\tFinish\tWaiting\tTurnaround\n");
    
    for (int i = 0; i < n; i++) {
        if (current_time < processes[i].arrival_time) {
            current_time = processes[i].arrival_time;
        }
        
        int start_time = current_time;
        processes[i].completion_time = current_time + processes[i].burst_time;
        processes[i].turnaround_time = 
            processes[i].completion_time - processes[i].arrival_time;
        processes[i].waiting_time = 
            processes[i].turnaround_time - processes[i].burst_time;
        
        total_wait += processes[i].waiting_time;
        total_turnaround += processes[i].turnaround_time;
        
        printf("P%d\t%d\t%d\t%d\t%d\t%d\t\t%d\n",
            processes[i].pid, processes[i].arrival_time,
            processes[i].burst_time, start_time,
            processes[i].completion_time, processes[i].waiting_time,
            processes[i].turnaround_time);
        
        current_time = processes[i].completion_time;
    }
    
    printf("\nAverage Waiting Time: %.2f", total_wait / n);
    printf("\nAverage Turnaround Time: %.2f", total_turnaround / n);
}


/* ---------- Shortest Job First (Non-preemptive) ---------- */
void sjf_schedule(Process processes[], int n) {
    printf("\n--- SJF (Shortest Job First) Scheduling ---\n");
    
    int completed = 0, current_time = 0;
    int is_completed[MAX_PROCESSES] = {0};
    float total_wait = 0, total_turnaround = 0;
    
    printf("PID\tArrival\tBurst\tFinish\tWaiting\tTurnaround\n");
    
    while (completed < n) {
        /* Find shortest job that has arrived and is not completed */
        int shortest = -1;
        int min_burst = INT_MAX;
        
        for (int i = 0; i < n; i++) {
            if (!is_completed[i] && processes[i].arrival_time <= current_time
                && processes[i].burst_time < min_burst) {
                min_burst = processes[i].burst_time;
                shortest = i;
            }
        }
        
        if (shortest == -1) {
            /* No process available — advance time */
            current_time++;
            continue;
        }
        
        /* Execute the shortest job */
        current_time += processes[shortest].burst_time;
        processes[shortest].completion_time = current_time;
        processes[shortest].turnaround_time = 
            current_time - processes[shortest].arrival_time;
        processes[shortest].waiting_time = 
            processes[shortest].turnaround_time - processes[shortest].burst_time;
        
        total_wait += processes[shortest].waiting_time;
        total_turnaround += processes[shortest].turnaround_time;
        is_completed[shortest] = 1;
        completed++;
        
        printf("P%d\t%d\t%d\t%d\t%d\t\t%d\n",
            processes[shortest].pid, processes[shortest].arrival_time,
            processes[shortest].burst_time, processes[shortest].completion_time,
            processes[shortest].waiting_time, processes[shortest].turnaround_time);
    }
    
    printf("\nAverage Waiting Time: %.2f", total_wait / n);
    printf("\nAverage Turnaround Time: %.2f", total_turnaround / n);
}


/* ---------- Round Robin Scheduling ---------- */
void rr_schedule(Process processes[], int n, int quantum) {
    printf("\n--- Round Robin Scheduling (Quantum=%d) ---\n", quantum);
    
    /* Create a copy with remaining time */
    Process *temp = malloc(n * sizeof(Process));
    memcpy(temp, processes, n * sizeof(Process));
    for (int i = 0; i < n; i++) {
        temp[i].remaining_time = temp[i].burst_time;
        temp[i].started = 0;
    }
    
    int queue[MAX_PROCESSES * 10];
    int front = 0, rear = 0;
    int current_time = 0, completed = 0;
    int in_queue[MAX_PROCESSES] = {0};
    float total_wait = 0, total_turnaround = 0;
    
    printf("PID\tArrival\tBurst\tFinish\tWaiting\tTurnaround\n");
    
    /* Add initial processes that arrive at time 0 */
    for (int i = 0; i < n; i++) {
        if (temp[i].arrival_time == 0) {
            queue[rear++] = i;
            in_queue[i] = 1;
        }
    }
    
    while (completed < n) {
        if (front == rear) {
            /* No process in queue — advance time */
            current_time++;
            /* Check for new arrivals */
            for (int i = 0; i < n; i++) {
                if (!in_queue[i] && temp[i].arrival_time <= current_time
                    && temp[i].remaining_time > 0) {
                    queue[rear++] = i;
                    in_queue[i] = 1;
                }
            }
            continue;
        }
        
        int idx = queue[front++];
        in_queue[idx] = 0;
        
        int exec_time = (temp[idx].remaining_time < quantum) 
                        ? temp[idx].remaining_time : quantum;
        temp[idx].remaining_time -= exec_time;
        current_time += exec_time;
        
        /* Check for new arrivals during this quantum */
        for (int i = 0; i < n; i++) {
            if (!in_queue[i] && temp[i].arrival_time > current_time - exec_time
                && temp[i].arrival_time <= current_time 
                && temp[i].remaining_time > 0) {
                queue[rear++] = i;
                in_queue[i] = 1;
            }
        }
        
        if (temp[idx].remaining_time == 0) {
            /* Process completed */
            temp[idx].completion_time = current_time;
            temp[idx].turnaround_time = 
                current_time - temp[idx].arrival_time;
            temp[idx].waiting_time = 
                temp[idx].turnaround_time - temp[idx].burst_time;
            
            total_wait += temp[idx].waiting_time;
            total_turnaround += temp[idx].turnaround_time;
            completed++;
            
            printf("P%d\t%d\t%d\t%d\t%d\t\t%d\n",
                temp[idx].pid, temp[idx].arrival_time,
                temp[idx].burst_time, temp[idx].completion_time,
                temp[idx].waiting_time, temp[idx].turnaround_time);
        } else {
            /* Re-add to queue */
            queue[rear++] = idx;
            in_queue[idx] = 1;
        }
    }
    
    printf("\nAverage Waiting Time: %.2f", total_wait / n);
    printf("\nAverage Turnaround Time: %.2f", total_turnaround / n);
    free(temp);
}


/* ---------- Priority Scheduling (Non-preemptive) ---------- */
void priority_schedule(Process processes[], int n) {
    printf("\n--- Priority Scheduling (Lower = Higher Priority) ---\n");
    
    int completed = 0, current_time = 0;
    int is_completed[MAX_PROCESSES] = {0};
    float total_wait = 0, total_turnaround = 0;
    
    printf("PID\tArrival\tBurst\tPriority\tFinish\tWaiting\tTurnaround\n");
    
    while (completed < n) {
        /* Find highest-priority (lowest number) arrived process */
        int highest = -1;
        int max_priority = INT_MAX;
        
        for (int i = 0; i < n; i++) {
            if (!is_completed[i] && processes[i].arrival_time <= current_time
                && processes[i].priority < max_priority) {
                max_priority = processes[i].priority;
                highest = i;
            }
        }
        
        if (highest == -1) {
            current_time++;
            continue;
        }
        
        current_time += processes[highest].burst_time;
        processes[highest].completion_time = current_time;
        processes[highest].turnaround_time = 
            current_time - processes[highest].arrival_time;
        processes[highest].waiting_time = 
            processes[highest].turnaround_time - processes[highest].burst_time;
        
        total_wait += processes[highest].waiting_time;
        total_turnaround += processes[highest].turnaround_time;
        is_completed[highest] = 1;
        completed++;
        
        printf("P%d\t%d\t%d\t%d\t\t%d\t%d\t\t%d\n",
            processes[highest].pid, processes[highest].arrival_time,
            processes[highest].burst_time, processes[highest].priority,
            processes[highest].completion_time, processes[highest].waiting_time,
            processes[highest].turnaround_time);
    }
    
    printf("\nAverage Waiting Time: %.2f", total_wait / n);
    printf("\nAverage Turnaround Time: %.2f", total_turnaround / n);
}


/* ===== DEMO ===== */
int main() {
    printf("=");
    for (int i = 0; i < 54; i++) printf("=");
    printf("\n");
    printf("   CPU SCHEDULING ALGORITHMS — DEMO\n");
    for (int i = 0; i < 54; i++) printf("=");
    printf("=\n");
    
    /* Define sample processes */
    Process processes[MAX_PROCESSES] = {
        {1, 0, 6, 2},
        {2, 2, 4, 4},
        {3, 4, 2, 1},
        {4, 5, 8, 3},
        {5, 7, 3, 5}
    };
    int n = 5;
    
    /* We need fresh copies for each algorithm since they modify in-place */
    Process copy[MAX_PROCESSES];
    
    memcpy(copy, processes, n * sizeof(Process));
    fcfs_schedule(copy, n);
    
    memcpy(copy, processes, n * sizeof(Process));
    sjf_schedule(copy, n);
    
    memcpy(copy, processes, n * sizeof(Process));
    rr_schedule(copy, n, 3);
    
    memcpy(copy, processes, n * sizeof(Process));
    priority_schedule(copy, n);
    
    printf("\n💡 Key takeaway: OS scheduling algorithms directly\n");
    printf("   impact system performance and user experience.\n");
    printf("   Linux uses CFS (Completely Fair Scheduler).\n");
    
    return 0;
}
