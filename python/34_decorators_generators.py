# ============================================================
# Program Title : Decorators & Generators Deep Dive
# Author        : Lydia S. Makiwa
# Date          : 2026-05-02
# Description   : Advanced Python patterns: timing decorators,
#                 retry logic, generator pipelines, context mgrs.
# ============================================================

import time
import functools
from contextlib import contextmanager

# 1. Timing decorator
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"  {func.__name__}() -> {time.perf_counter()-t0:.6f}s")
        return result
    return wrapper

# 2. Retry decorator
def retry(attempts=3, delay=0):
    def dec(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(1, attempts+1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"  attempt {i} failed: {e}")
                    time.sleep(delay)
            raise RuntimeError(f"{func.__name__} failed after {attempts} tries")
        return wrapper
    return dec

# 3. Generator pipeline
def integers(start=1):
    n = start
    while True:
        yield n
        n += 1

def take(n, it):
    for i, v in enumerate(it):
        if i >= n: break
        yield v

def only_even(it):
    for v in it:
        if v % 2 == 0: yield v

# 4. Context manager
@contextmanager
def managed(name):
    print(f"  [OPEN]  {name}")
    try:
        yield name.upper()
    finally:
        print(f"  [CLOSE] {name}")


# -- Demo ------------------------------------------------------
if __name__ == "__main__":
    @timer
    def big_sum(n): return sum(range(n))

    print("1. Timer:")
    big_sum(1_000_000)

    _calls = [0]
    @retry(attempts=3, delay=0)
    def flaky():
        _calls[0] += 1
        if _calls[0] < 3: raise ValueError("not ready")
        return "success!"

    print("\n2. Retry:")
    print(" ", flaky())

    print("\n3. Generator pipeline (first 6 evens):")
    print(" ", list(take(6, only_even(integers()))))

    print("\n4. Context manager:")
    with managed("db_connection") as res:
        print(f"  using: {res}")
