# Program Title: Interval Tree & Merge Intervals
# Author: Lydia S. Makiwa
# Date: 2026-05-05
# Description: Implements interval merging and overlap detection.
#              Used in scheduling, calendar apps, genome analysis,
#              and segment overlap problems.

def merge_intervals(intervals):
    """Merge all overlapping intervals. O(n log n)."""
    if not intervals: return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged

def insert_interval(intervals, new_interval):
    """Insert a new interval and merge. O(n)."""
    result = []
    i, n   = 0, len(intervals)
    # Add all intervals that end before new_interval starts
    while i < n and intervals[i][1] < new_interval[0]:
        result.append(intervals[i]); i += 1
    # Merge overlapping intervals
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    result.append(new_interval)
    result.extend(intervals[i:])
    return result

def count_non_overlapping(intervals):
    """Greedy: max number of non-overlapping intervals (Activity Selection)."""
    intervals.sort(key=lambda x: x[1])  # sort by end time
    count, last_end = 0, float('-inf')
    selected = []
    for s, e in intervals:
        if s >= last_end:
            selected.append([s, e])
            last_end = e
            count += 1
    return count, selected

def min_rooms_needed(intervals):
    """Minimum meeting rooms required for all intervals."""
    import heapq
    intervals.sort(key=lambda x: x[0])
    heap = []  # min-heap of end times
    for s, e in intervals:
        if heap and heap[0] <= s:
            heapq.heapreplace(heap, e)
        else:
            heapq.heappush(heap, e)
    return len(heap)

# ─── Demo ───
raw = [[1,3],[2,6],[8,10],[15,18],[7,9]]
print("Original intervals:", raw)
print("Merged:            ", merge_intervals([list(x) for x in raw]))

intervals_sorted = [[1,2],[3,5],[6,7],[8,10],[12,16]]
print("\nInsert [4,8] into", intervals_sorted)
print("Result:           ", insert_interval([list(x) for x in intervals_sorted], [4,8]))

meetings = [[0,30],[5,10],[15,20],[25,35],[10,40]]
print("\nMeetings:", meetings)
cnt, sel = count_non_overlapping([list(x) for x in meetings])
print(f"Max non-overlapping: {cnt}  →  {sel}")
print(f"Min rooms needed:    {min_rooms_needed([list(x) for x in meetings])}")
