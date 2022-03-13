# We will use Segment Tree 07 here, but use first below (<= v) instead of first above
# So, we will use segment tree on min and for each query we apply first_below function until we can.
# Notice that we will destroy no more than created building, so we will run first_below no more than m times.

class SegmentTree:
    def __init__(self, n, arr):
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.T = [0] * (2 * self.size - 1)
        self.arr = arr

    def _build(self, x, lx, rx):
        if rx - lx == 1:
            if lx < len(self.arr):
                self.T[x] = self.arr[lx]
        else:
            mx = (lx + rx) // 2
            self._build(2 * x + 1, lx, mx)
            self._build(2 * x + 2, mx, rx)
            self.T[x] = min(self.T[2 * x + 1], self.T[2 * x + 2])

    def build(self):
        self._build(0, 0, self.size)

    def _set(self, i, v, x, lx, rx):
        if rx - lx == 1:
            self.T[x] = v
            return
        mx = (lx + rx) // 2
        if i < mx:
            self._set(i, v, 2 * x + 1, lx, mx)
        else:
            self._set(i, v, 2 * x + 2, mx, rx)
        self.T[x] = min(self.T[2 * x + 1], self.T[2 * x + 2])

    def set(self, i, v):
        self._set(i, v, 0, 0, self.size)

    def first_below_(self, v, l, x, lx, rx):
        if self.T[x] > v or rx <= l:
            return -1
        if rx - lx == 1:
            return lx
        mx = (lx + rx) // 2
        res = self.first_below_(v, l, 2 * x + 1, lx, mx)
        if res == -1:
            res = self.first_below_(v, l, 2 * x + 2, mx, rx)
        return res

    def first_below(self, v, l):
        return self.first_below_(v, l, 0, 0, self.size)

import io, os, sys
input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline


if __name__ == '__main__':
    n, m = [int(i) for i in input().split()]
    STree = SegmentTree(n, [float("inf")] * n)
    STree.build()

    for i in range(m):
        t = [int(i) for i in input().split()]
        if t[0] == 1:
            STree.set(t[1], t[2])
        else:
            l, r, p = t[1], t[2], t[3]
            destroyed = 0
            while True:
                idx = STree.first_below(p, l)
                if idx == -1 or idx >= r:
                    break
                STree.set(idx, float("inf"))
                destroyed += 1
            print(destroyed)
