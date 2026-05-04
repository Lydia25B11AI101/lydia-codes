# ============================================================
# Program Title : Q-Learning Reinforcement Learning Demo
# Author        : Lydia S. Makiwa
# Date          : 2026-05-04
# Description   : Teach an agent to navigate a 4x4 grid
#                 to reach a goal using Q-learning.
# ============================================================

import numpy as np

# 4x4 grid world: 0=open, -1=hole, 1=goal
GRID = [
    [0,  0,  0,  0],
    [0, -1,  0, -1],
    [0,  0,  0, -1],
    [-1, 0,  0,  1],
]
ROWS, COLS = 4, 4
ACTIONS = [(-1,0),(1,0),(0,-1),(0,1)]  # up down left right
ACTION_NAMES = ['UP','DOWN','LEFT','RIGHT']

def step(state, action):
    r, c = state
    dr, dc = ACTIONS[action]
    nr, nc = max(0,min(ROWS-1,r+dr)), max(0,min(COLS-1,c+dc))
    cell = GRID[nr][nc]
    if cell == -1:
        return (nr,nc), -1, True
    if cell == 1:
        return (nr,nc), 10, True
    return (nr,nc), -0.1, False

# Q-table: states x actions
Q = np.zeros((ROWS*COLS, 4))
def idx(s): return s[0]*COLS + s[1]

# Hyperparameters
alpha, gamma, eps, episodes = 0.8, 0.95, 0.1, 5000
np.random.seed(42)

for ep in range(episodes):
    state = (0, 0)
    for _ in range(100):
        if np.random.rand() < eps:
            action = np.random.randint(4)
        else:
            action = np.argmax(Q[idx(state)])
        next_s, reward, done = step(state, action)
        Q[idx(state), action] += alpha * (
            reward + gamma * np.max(Q[idx(next_s)]) - Q[idx(state), action])
        state = next_s
        if done:
            break

# Show learned policy
print('Learned policy grid (U=Up D=Down L=Left R=Right G=Goal H=Hole):')
symbols = ['U','D','L','R']
for r in range(ROWS):
    row = ''
    for c in range(COLS):
        if GRID[r][c] == -1:
            row += ' H '
        elif GRID[r][c] == 1:
            row += ' G '
        else:
            row += f' {symbols[np.argmax(Q[idx((r,c))])]} '
    print(row)
print('Q-Learning complete!')
