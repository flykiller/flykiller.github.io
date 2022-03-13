# this segment tree will support two operations:
# 1. Set element i equal to v.
# 2. Find sum of inversions in [l, r] given that values are small: <= 40
# for each segment keep counter of frequencies T and number of inversions I
# then we can combine two nodes in `O(40)` time. Total complexity of one operation is O(40 * log n).

from itertools import accumulate

class SegmentTree:
    def __init__(self, n, arr):
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.T = [[0]*40 for _ in range(2 * self.size - 1)]
        self.I = [0] * (2 * self.size - 1)
        self.arr = arr

    def combine(self, x, y):
        return sum(i*j for i, j in zip(x[1:], accumulate(y)))

    def sum_cnt(self, x, y):
        return [i + j for i, j in zip(x, y)]

    def _build(self, x, lx, rx):
        if rx - lx == 1:
            if lx < len(self.arr):
                self.T[x][self.arr[lx] - 1] += 1
        else:
            mx = (lx + rx)//2
            self._build(2*x+1, lx, mx)
            self._build(2*x+2, mx, rx)
            self.T[x] = self.sum_cnt(self.T[2 * x + 1], self.T[2 * x + 2])
            self.I[x] = self.I[2 * x + 1] + self.I[2 * x + 2] + self.combine(self.T[2 * x + 1], self.T[2 * x + 2])

    def build(self):
        self._build(0, 0, self.size)

    def _set(self, i, v, x, lx, rx):
        if rx - lx == 1:
            self.T[x] = [0]*40
            self.T[x][v-1] += 1
            return
        mx = (lx + rx) // 2
        if i < mx:
            self._set(i, v, 2 * x + 1, lx, mx)
        else:
            self._set(i, v, 2 * x + 2, mx, rx)
        self.T[x] = self.sum_cnt(self.T[2 * x + 1], self.T[2 * x + 2])
        self.I[x] = self.I[2 * x + 1] + self.I[2 * x + 2] + self.combine(self.T[2 * x + 1], self.T[2 * x + 2])

    def set(self, i, v):
        self._set(i, v, 0, 0, self.size)

    def _inversions(self, l, r, x, lx, rx):
        if l >= rx or lx >= r:
            return [0]*40, 0
        if lx >= l and rx <= r:
            return self.T[x], self.I[x]
        mx = (lx + rx) // 2
        T1, I1 = self._inversions(l, r, 2 * x + 1, lx, mx)
        T2, I2 = self._inversions(l, r, 2 * x + 2, mx, rx)
        return self.sum_cnt(T1, T2), I1 + I2 + self.combine(T1, T2)

    def inversions(self, l, r):
        return self._inversions(l, r, 0, 0, self.size)

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
            print(STree.inversions(t[1]-1, t[2])[1])