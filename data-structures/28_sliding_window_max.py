# Program Title: Sliding Window Maximum (Monotonic Deque)
# Author: Lydia S. Makiwa
# Date: 2026-05-05
# Description: Finds the maximum value in every sliding window of size k
#              in O(n) time using a monotonic deque.
#              Classic interview problem — used in signal processing & stream analytics.

from collections import deque

def sliding_window_max(nums, k):
    """
    Returns a list of max values for each window of size k.
    Uses a monotonic decreasing deque storing indices.
    """
    dq  = deque()   # stores indices, front = index of current max
    result = []

    for i, val in enumerate(nums):
        # Remove elements outside the window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Maintain decreasing order — pop smaller elements from back
        while dq and nums[dq[-1]] < val:
            dq.pop()

        dq.append(i)

        # Window is fully formed
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result

def sliding_window_min(nums, k):
    """Sliding window minimum — monotonic INCREASING deque."""
    dq, result = deque(), []
    for i, val in enumerate(nums):
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        while dq and nums[dq[-1]] > val:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result

# ─── Demo ───
nums = [3, 1, 2, 5, 8, 4, 6, 7, 2, 9]
k    = 3

print(f"Array:  {nums}")
print(f"Window: k={k}")
print(f"Max:    {sliding_window_max(nums, k)}")
print(f"Min:    {sliding_window_min(nums, k)}")

print("\nAll windows:")
for i in range(len(nums) - k + 1):
    window = nums[i:i+k]
    print(f"  {window}  max={max(window)}  min={min(window)}")
