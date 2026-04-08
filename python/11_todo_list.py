# Python Program 11: Command-Line To-Do List
# Author: Lydia S. Makiwa
# Description: A simple persistent to-do list app using a text file

import os

FILE = "todos.txt"

def load_todos():
    if not os.path.exists(FILE): return []
    with open(FILE) as f:
        return [line.strip() for line in f if line.strip()]

def save_todos(todos):
    with open(FILE, 'w') as f:
        f.write('\n'.join(todos))

def show_todos(todos):
    if not todos:
        print("  📭 No tasks yet!")
        return
    for i, task in enumerate(todos, 1):
        status = "✅" if task.startswith("[done]") else "⬜"
        label = task.replace("[done]", "").strip()
        print(f"  {i}. {status} {label}")

todos = load_todos()
while True:
    print("\n=== To-Do List ===")
    show_todos(todos)
    print("\n[1] Add  [2] Done  [3] Delete  [4] Quit")
    choice = input("Choice: ").strip()

    if choice == '1':
        task = input("New task: ").strip()
        if task: todos.append(task); save_todos(todos)
    elif choice == '2':
        idx = int(input("Mark done (number): ")) - 1
        if 0 <= idx < len(todos):
            todos[idx] = "[done] " + todos[idx].replace("[done]","").strip()
            save_todos(todos)
    elif choice == '3':
        idx = int(input("Delete (number): ")) - 1
        if 0 <= idx < len(todos):
            removed = todos.pop(idx); save_todos(todos)
            print(f"Deleted: {removed}")
    elif choice == '4':
        print("Goodbye! 👋"); break
