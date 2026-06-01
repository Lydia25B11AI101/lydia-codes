"""
Program  : 32_n_queens_problem.py
Title    : N-Queens Problem — Classic Backtracking
Author   : Lydia S. Makiwa
Date     : 2026-06-01

Description:
    Solves the N-Queens problem where N queens must be placed
    on an N×N chessboard so no two queens attack each other.
    Uses backtracking with constraint propagation for efficiency.
    This problem is a classic in AI and combinatorial optimisation,
    illustrating constraint satisfaction and search pruning.
"""


class NQueensSolver:
    """
    Solves the N-Queens problem with multiple output formats.
    """
    
    def __init__(self, n):
        self.n = n
        self.solutions = []  # All valid board configurations
        self.backtrack_count = 0  # For performance tracking
    
    def solve(self):
        """
        Find all solutions to the N-Queens problem.
        
        Uses backtracking with three constraint sets for
        O(1) conflict checking:
            - cols: which columns are occupied
            - diag1: row+col (NW-SE diagonals)
            - diag2: row-col (NE-SW diagonals)
        """
        self.solutions = []
        self.backtrack_count = 0
        
        # Constraint sets for O(1) conflict checking
        cols = set()
        diag1 = set()  # (row + col) = constant on NW-SE diagonal
        diag2 = set()  # (row - col) = constant on NE-SW diagonal
        
        # Current queen positions: board[row] = col
        board = [-1] * self.n
        
        def place_queen(row):
            """Try to place a queen at given row."""
            if row == self.n:
                # All queens placed — found a solution
                self.solutions.append(board[:])
                return
            
            for col in range(self.n):
                d1 = row + col
                d2 = row - col
                
                # Check constraints
                if col in cols or d1 in diag1 or d2 in diag2:
                    self.backtrack_count += 1
                    continue
                
                # Place queen
                board[row] = col
                cols.add(col)
                diag1.add(d1)
                diag2.add(d2)
                
                # Recurse to next row
                place_queen(row + 1)
                
                # Remove queen (backtrack)
                cols.remove(col)
                diag1.remove(d1)
                diag2.remove(d2)
                board[row] = -1
        
        place_queen(0)
        return self.solutions
    
    def get_solution_count(self):
        """Return number of solutions found."""
        return len(self.solutions)
    
    @staticmethod
    def board_to_grid(board):
        """
        Convert board positions list to 2D grid.
        board[row] = col means a queen is at (row, col).
        Returns list of strings: 'Q' for queen, '.' for empty.
        """
        n = len(board)
        grid = []
        for row in range(n):
            line = ""
            for col in range(n):
                line += "Q " if board[row] == col else ". "
            grid.append(line.rstrip())
        return grid
    
    def print_solution(self, board, board_number=1):
        """Print a single solution as a chessboard."""
        n = len(board)
        print(f"\n   Solution #{board_number}:")
        print("   " + "---" * n)
        for row in range(n):
            print("   |", end="")
            for col in range(n):
                if board[row] == col:
                    print("♛ ", end="")
                else:
                    print("· ", end="")
            print("|")
        print("   " + "---" * n)
    
    def print_board_positions(self, board):
        """Print queen positions as (row, col) coordinates."""
        positions = [(r, c) for r, c in enumerate(board)]
        return positions
    
    def is_safe(self, board, row, col):
        """Check if a position is safe given existing placements."""
        for prev_row in range(row):
            prev_col = board[prev_row]
            # Same column or same diagonal
            if (prev_col == col or 
                abs(prev_row - row) == abs(prev_col - col)):
                return False
        return True
    
    def first_solution(self):
        """Fast solver that stops at the first solution found."""
        board = [-1] * self.n
        
        def solve(row):
            if row == self.n:
                return True
            for col in range(self.n):
                if self.is_safe(board, row, col):
                    board[row] = col
                    if solve(row + 1):
                        return True
                    board[row] = -1
            return False
        
        solve(0)
        return board if -1 not in board else None
    
    def count_solutions_for_n(self, max_n=12):
        """Count solutions for N from 1 to max_n."""
        print(f"   {'N':>3s} | {'Solutions':>10s} | {'Backtracks':>10s}")
        print("   " + "-" * 30)
        for n in range(1, min(max_n + 1, 13)):
            solver = NQueensSolver(n)
            solutions = solver.solve()
            print(f"   {n:3d} | {len(solutions):10d} | {solver.backtrack_count:10d}")


def run_fast_solve_comparison():
    """Compare the two solving approaches."""
    print("\n📊 Approach Comparison (N=8):")
    print("   Constraint-propagation vs. Naive backtracking")
    
    n = 8
    solver = NQueensSolver(n)
    solutions = solver.solve()
    print(f"   Constraint-based: {len(solutions)} solutions")
    print(f"   Total checks: {solver.backtrack_count}")


# ===== DEMO =====
if __name__ == "__main__":
    print("=" * 55)
    print("   N-QUEENS PROBLEM — BACKTRACKING DEMO")
    print("=" * 55)
    
    # Demo 1: Classic 4-Queens
    print("\n👑 Demo 1: 4-Queens (classic teaching example)")
    solver = NQueensSolver(4)
    solutions = solver.solve()
    print(f"   Found {len(solutions)} solutions for 4×4 board")
    
    for i, board in enumerate(solutions[:2], 1):
        solver.print_solution(board, i)
        positions = solver.print_board_positions(board)
        print(f"   Queens at: {positions}")
    
    # Demo 2: 8-Queens (standard chessboard)
    print("\n👑 Demo 2: 8-Queens (standard chessboard)")
    solver = NQueensSolver(8)
    solutions = solver.solve()
    print(f"   Found {len(solutions)} solutions for 8×8 board")
    print(f"   Number of backtracks: {solver.backtrack_count}")
    
    # Show first 3 solutions
    for i in range(3):
        solver.print_solution(solutions[i], i + 1)
        positions = solver.print_board_positions(solutions[i])
        print(f"   Queens at: {positions}")
    
    # Demo 3: Quick first solution for larger boards
    print("\n👑 Demo 3: First solution for larger boards")
    for n in [10, 12]:
        solver = NQueensSolver(n)
        board = solver.first_solution()
        if board:
            print(f"   {n}×{n}: First solution found")
            print(f"   Queens: {solver.print_board_positions(board)}")
    
    # Demo 4: Solution count by N
    print("\n📊 Demo 4: Solution count scaling")
    solver = NQueensSolver(4)
    solver.count_solutions_for_n(10)
    
    print("\n💡 N-Queens teaches: constraint satisfaction,")
    print("   search space pruning, and is a benchmark for")
    print("   CSP (Constraint Satisfaction Problem) solvers!")
