# Data Structure 12: Two Sum Problem (LeetCode Style)
# Author: Lydia S. Makiwa
# Description: Find two numbers that add up to a target — O(n) with hash map

def two_sum_brute(nums, target):
    """Brute force O(n²)"""
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []

def two_sum_hashmap(nums, target):
    """Optimised O(n) using hash map"""
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# Demo
test_cases = [
    ([2, 7, 11, 15], 9),
    ([3, 2, 4], 6),
    ([1, 5, 3, 8, 2], 10),
]

print("=== Two Sum Problem ===\n")
for nums, target in test_cases:
    brute  = two_sum_brute(nums, target)
    hashmp = two_sum_hashmap(nums, target)
    print(f"nums={nums}, target={target}")
    print(f"  Brute Force : indices {brute}  → {nums[brute[0]]} + {nums[brute[1]]} = {target}")
    print(f"  Hash Map    : indices {hashmp} → {nums[hashmp[0]]} + {nums[hashmp[1]]} = {target}\n")
