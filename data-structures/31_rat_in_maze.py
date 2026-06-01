"""
Program  : 31_rat_in_maze.py
Title    : Rat in a Maze — Backtracking Algorithm
Author   : Lydia S. Makiwa
Date     : 2026-06-01

Description:
    Solves the classic Rat in a Maze problem using backtracking.
    The rat starts at (0,0) and needs to reach (n-1,n-1) moving
    only right or down through open cells (1s). This demonstrates
    the backtracking paradigm: try a path, if it fails, undo
    and try another. Foundational for AI pathfinding, robotics
    navigation, and game development.
"""


def solve_maze(maze):
    """
    Solve the Rat in a Maze problem using backtracking.
    
    The maze is an n×n grid where:
        1 = open path (rat can move here)
        0 = blocked cell
    
    The rat can only move RIGHT or DOWN.
    
    Args:
        maze: 2D list representing the maze
    
    Returns:
        solved: 2D list showing the solution path (1s) or None
        moves: list of (row, col) steps in the solution
    """
    n = len(maze)
    
    # Safety check: start and end must be open
    if maze[0][0] == 0 or maze[n-1][n-1] == 0:
        return None, []
    
    # Solution grid — will mark 1s for the chosen path
    solution = [[0] * n for _ in range(n)]
    move_history = []
    
    def is_safe(row, col):
        """Check if (row, col) is within bounds and open."""
        return (0 <= row < n and 0 <= col < n and maze[row][col] == 1)
    
    def solve(row, col):
        """
        Recursive backtracking solver.
        Returns True if a path is found from (row, col) to exit.
        """
        # Base case: reached the bottom-right corner
        if row == n - 1 and col == n - 1:
            solution[row][col] = 1
            move_history.append((row, col))
            return True
        
        # Try this cell
        if is_safe(row, col):
            solution[row][col] = 1
            move_history.append((row, col))
            
            # Try moving RIGHT (col + 1)
            if solve(row, col + 1):
                return True
            
            # Try moving DOWN (row + 1)
            if solve(row + 1, col):
                return True
            
            # BACKTRACK: This path doesn't work
            solution[row][col] = 0
            move_history.pop()
            return False
        
        return False
    
    if solve(0, 0):
        return solution, move_history
    else:
        return None, []


def solve_maze_all_paths(maze):
    """Find ALL possible paths from start to exit."""
    n = len(maze)
    all_paths = []
    
    def explore(row, col, path, visited):
        """DFS to find all paths."""
        if row == n - 1 and col == n - 1:
            all_paths.append(path + [(row, col)])
            return
        
        if not (0 <= row < n and 0 <= col < n):
            return
        if maze[row][col] == 0 or (row, col) in visited:
            return
        
        visited.add((row, col))
        new_path = path + [(row, col)]
        
        # Try all 4 directions for all-paths version
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            explore(row + dr, col + dc, new_path, visited)
        
        visited.remove((row, col))
    
    explore(0, 0, [], set())
    return all_paths


def print_maze(maze, solution=None, path=None):
    """Pretty print the maze, optionally with solution overlay."""
    n = len(maze)
    
    path_set = set(path) if path else set()
    solution_set = set()
    if solution:
        for i in range(n):
            for j in range(n):
                if solution[i][j] == 1:
                    solution_set.add((i, j))
    
    print("   " + "---" * n)
    for i in range(n):
        print("   |", end="")
        for j in range(n):
            cell = maze[i][j]
            is_path = (i, j) in path_set or (i, j) in solution_set
            
            if cell == 0:
                print("⬛", end="")  # Wall
            elif is_path:
                print("🐀", end="")  # Path taken
            else:
                print("  ", end="")  # Open but not in solution
        
        print("|")
    print("   " + "---" * n)
    
    if solution:
        print(f"   S = Start (0,0), E = Exit ({n-1},{n-1})")


# ===== DEMO =====
if __name__ == "__main__":
    print("=" * 55)
    print("   RAT IN A MAZE — BACKTRACKING DEMO")
    print("=" * 55)
    
    # Demo 1: Standard 5×5 maze
    print("\n🔍 Demo 1: Solving a 5×5 maze")
    maze1 = [
        [1, 0, 0, 0, 0],
        [1, 1, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 1, 1, 1],
        [0, 0, 0, 1, 1]
    ]
    
    print_maze(maze1)
    solution, moves = solve_maze(maze1)
    
    if solution:
        print(f"\n   ✅ Solution found! Path length: {len(moves)}")
        print(f"   Path: {' → '.join(str(m) for m in moves)}")
        print("\n   Solution grid (1 = path taken):")
        for row in solution:
            print(f"     {row}")
    else:
        print("\n   ❌ No solution exists!")
    
    # Demo 2: Maze with multiple paths
    print("\n🔍 Demo 2: Maze with multiple solutions")
    maze2 = [
        [1, 1, 1],
        [0, 1, 1],
        [0, 0, 1]
    ]
    
    print_maze(maze2)
    all_paths = solve_maze_all_paths(maze2)
    print(f"   Found {len(all_paths)} possible paths:")
    for i, p in enumerate(all_paths, 1):
        print(f"   Path {i}: {' → '.join(str(m) for m in p)}")
    
    # Demo 3: No solution
    print("\n🔍 Demo 3: Maze with no solution")
    maze3 = [
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 0]  # Exit (2,2) is blocked
    ]
    
    print_maze(maze3)
    solution, moves = solve_maze(maze3)
    if not solution:
        print("   ❌ No solution — exit cell is blocked!")
    
    # Demo 4: Debug mode showing backtracking
    print("\n🔍 Demo 4: Tracing backtracking steps")
    maze4 = [
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 1]
    ]
    
    backtrack_steps = []
    
    def trace_solve(maze):
        n = len(maze)
        sol = [[0]*n for _ in range(n)]
        
        def solve(r, c):
            if r == n-1 and c == n-1:
                sol[r][c] = 1
                backtrack_steps.append(f"🏁 Reached exit at ({r},{c})")
                return True
            
            if 0 <= r < n and 0 <= c < n and maze[r][c] == 1 and sol[r][c] == 0:
                sol[r][c] = 1
                backtrack_steps.append(f"👉 Try ({r},{c})")
                
                # Try RIGHT, DOWN, LEFT, UP (allowing all 4 directions)
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    if solve(r + dr, c + dc):
                        return True
                
                sol[r][c] = 0
                backtrack_steps.append(f"↩ Backtrack from ({r},{c})")
                return False
            return False
        
        solve(0, 0)
        return sol
    
    trace_solve(maze4)
    for step in backtrack_steps:
        print(f"   {step}")
    
    print("\n💡 Backtracking is used in: puzzle solvers (Sudoku),")
    print("   constraint satisfaction, AI game players (chess),")
    print("   and compiler parsing (recursive descent)!")
