# this segment tree will support two operations:
# 1. Set element i equal to v.
# 2. Find number of different elements in [l, r] given that values are small: <= 40
# for each segment keep counter of frequencies T
# then we can combine two nodes in `O(40)` time. Total complexity of one operation is O(40 * log n).

from itertools import accumulate
from collections import Counter

class SegmentTree:
    def __init__(self, n, arr):
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.T = [Counter() for _ in range(2 * self.size - 1)]
        self.arr = arr

    def _build(self, x, lx, rx):
        if rx - lx == 1:
            if lx < len(self.arr):
                self.T[x][self.arr[lx] - 1] += 1
        else:
            mx = (lx + rx)//2
            self._build(2*x+1, lx, mx)
            self._build(2*x+2, mx, rx)
            self.T[x] = self.T[2 * x + 1] + self.T[2 * x + 2]

    def build(self):
        self._build(0, 0, self.size)

    def _set(self, i, v, x, lx, rx):
        if rx - lx == 1:
            self.T[x] = Counter()
            self.T[x][v-1] += 1
            return
        mx = (lx + rx) // 2
        if i < mx:
            self._set(i, v, 2 * x + 1, lx, mx)
        else:
            self._set(i, v, 2 * x + 2, mx, rx)
        self.T[x] = self.T[2 * x + 1] + self.T[2 * x + 2]

    def set(self, i, v):
        self._set(i, v, 0, 0, self.size)

    def _cnt_different(self, l, r, x, lx, rx):
        if l >= rx or lx >= r:
            return Counter()
        if lx >= l and rx <= r:
            return self.T[x]
        mx = (lx + rx) // 2
        T1 = self._cnt_different(l, r, 2 * x + 1, lx, mx)
        T2 = self._cnt_different(l, r, 2 * x + 2, mx, rx)
        return T1 + T2

    def cnt_different(self, l, r):
        return self._cnt_different(l, r, 0, 0, self.size)

import io, os, sys
input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline

if __name__ == '__main__':
    n, m = [int(i) for i in input().split()]
    arr = [int(i) for i in input().split()]
    STree = SegmentTree(n, arr)
    STree.build()

    for i in range(m):
        t = [int(i) for i in input().split()]
        if t[0] == 2:
            STree.set(t[1]-1, t[2])
        else:
            ans = STree.cnt_different(t[1]-1, t[2])
            print(len(ans))