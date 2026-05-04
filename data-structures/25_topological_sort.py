# ============================================================
# Program Title : Topological Sort (Kahn's BFS Algorithm)
# Author        : Lydia S. Makiwa
# Date          : 2026-05-04
# Description   : Sort a DAG's nodes in topological order
#                 using in-degree counts (Kahn's algorithm).
#                 Essential for scheduling / build systems.
# ============================================================

from collections import deque, defaultdict

def topological_sort(n, edges):
    graph    = defaultdict(list)
    in_degree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    if len(order) != n:
        return None  # cycle detected
    return order

# Demo: course prerequisites
# 0=Maths, 1=CS101, 2=Algorithms, 3=ML, 4=DL, 5=Capstone
courses = ['Maths','CS101','Algorithms','ML','DL','Capstone']
prereqs = [(0,1),(0,2),(1,2),(2,3),(3,4),(2,4),(3,5),(4,5)]

order = topological_sort(len(courses), prereqs)
if order:
    print('Study order:')
    for i, idx in enumerate(order, 1):
        print(f'  Step {i}: {courses[idx]}')
else:
    print('Cycle detected — invalid course graph!')

# Cycle detection demo
cyclic = [(0,1),(1,2),(2,0)]
result = topological_sort(3, cyclic)
print('Cyclic graph result:', result)
print('Topological sort complete!')
