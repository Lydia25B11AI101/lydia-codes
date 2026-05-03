# ============================================================
# Program Title : Segment Tree (Range Sum & Point Update)
# Author        : Lydia S. Makiwa
# Date          : 2026-05-03
# Description   : Efficient range-sum queries and point updates
#                 in O(log n) time using a Segment Tree.
# ============================================================

class SegmentTree:
    """Segment Tree supporting range sum queries and point updates."""

    def __init__(self, data: list):
        self.n    = len(data)
        self.tree = [0] * (4 * self.n)
        self._build(data, 0, 0, self.n - 1)

    # ── Internal helpers ──────────────────────────────────────
    def _build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            self._build(data, 2*node+1, start,   mid)
            self._build(data, 2*node+2, mid+1, end)
            self.tree[node] = self.tree[2*node+1] + self.tree[2*node+2]

    def _update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self._update(2*node+1, start,   mid, idx, val)
            else:
                self._update(2*node+2, mid+1, end, idx, val)
            self.tree[node] = self.tree[2*node+1] + self.tree[2*node+2]

    def _query(self, node, start, end, l, r):
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return (self._query(2*node+1, start,   mid, l, r) +
                self._query(2*node+2, mid+1, end, l, r))

    # ── Public API ────────────────────────────────────────────
    def update(self, idx: int, val: int):
        """Set data[idx] = val and update the tree."""
        self._update(0, 0, self.n-1, idx, val)

    def query(self, l: int, r: int) -> int:
        """Return sum of data[l..r] (inclusive, 0-indexed)."""
        return self._query(0, 0, self.n-1, l, r)


# ── Demo ─────────────────────────────────────────────────────
if __name__ == "__main__":
    data = [1, 3, 5, 7, 9, 11]
    st   = SegmentTree(data)

    print("Segment Tree Demo")
    print("=" * 40)
    print(f"Array : {data}")
    print(f"Sum [0,2] = {st.query(0, 2)}")   # 1+3+5 = 9
    print(f"Sum [1,4] = {st.query(1, 4)}")   # 3+5+7+9 = 24
    print(f"Sum [0,5] = {st.query(0, 5)}")   # total = 36

    print("\nUpdating index 2: 5 → 10")
    st.update(2, 10)
    print(f"Sum [0,2] = {st.query(0, 2)}")   # 1+3+10 = 14
    print(f"Sum [0,5] = {st.query(0, 5)}")   # 41
