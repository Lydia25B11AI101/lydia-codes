# ============================================================
# Program Title : Genetic Algorithm - Function Optimisation
# Author        : Lydia S. Makiwa
# Date          : 2026-05-04
# Description   : Find max of f(x)=x*sin(10*pi*x)+1 on [-1,2]
#                 using a genetic algorithm with selection,
#                 crossover, and mutation.
# ============================================================

import numpy as np
import math

def fitness(x):
    return x * math.sin(10 * math.pi * x) + 1.0

def decode(bits, lo=-1.0, hi=2.0):
    val = int(''.join(str(b) for b in bits), 2)
    return lo + (hi - lo) * val / (2**len(bits) - 1)

def crossover(p1, p2):
    pt = np.random.randint(1, len(p1))
    return (np.concatenate([p1[:pt], p2[pt:]]),
            np.concatenate([p2[:pt], p1[pt:]]))

def mutate(ind, rate=0.01):
    return np.array([1-b if np.random.rand() < rate else b for b in ind])

# GA hyper-parameters
POP_SIZE, BITS, GENS = 60, 20, 100
np.random.seed(0)
pop = np.random.randint(0, 2, (POP_SIZE, BITS))

for gen in range(GENS):
    scores = np.array([fitness(decode(ind)) for ind in pop])
    probs  = scores - scores.min() + 1e-6
    probs /= probs.sum()
    new_pop = []
    while len(new_pop) < POP_SIZE:
        i1, i2 = np.random.choice(POP_SIZE, 2, p=probs, replace=False)
        c1, c2  = crossover(pop[i1], pop[i2])
        new_pop += [mutate(c1), mutate(c2)]
    pop = np.array(new_pop[:POP_SIZE])

scores = np.array([fitness(decode(ind)) for ind in pop])
best   = pop[scores.argmax()]
x_best = decode(best)
print(f'Best x   : {x_best:.6f}')
print(f'Best f(x): {fitness(x_best):.6f}')
print('(Known global max approx 1.85 near x=1.85)')
print('Genetic algorithm complete!')
