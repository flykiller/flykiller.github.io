# this segment tree will support two operations:
# 1. set values in range [l, r) as arithmetic progression with parameters a, d or
# add value v to value in this range.
# 2. find maximum in range [l, r)

# In lazy updates we will keep pair (d, v) where d means that we need to set values to
# 0, d, 2d, ... and v means that after we add v to all values.
# If d = -inf, it means that we skip the first step.

from collections import defaultdict

class SegmentTree:
    def __init__(self, n):
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.ZERO = -float("inf")  # neutral element, for ma it is +inf
        self.NO_OPERATION = (float("inf"), 0)
        self.T = defaultdict(int)
        self.L = defaultdict(lambda: self.NO_OPERATION)

    def op_query(self, a, b):
        return max(a, b)

    def op_modify_L(self, h0, h1, len_):
        d, v = h1
        if d != -float("inf"):
            return d, v + d * len_
        else d == -float("inf"):
            if h0 != self.NO_OPERATION:
                return h0[0], h0[1] + v
            else:
                return h1

    def op_modify_T(self, x, h0, len_):
        d, v = h0
        if d != -float("inf"):
            return v + d * len_
        else:
            return x + v

    def propagate(self, x, lx, rx):
        if self.L[x] == self.NO_OPERATION or rx - lx == 1:
            return
        mx = (lx + rx) // 2
        d, v = self.L[x]
        self.L[2 * x + 1] = self.op_modify_L(self.L[2 * x + 1], self.L[x], 0)
        self.L[2 * x + 2] = self.op_modify_L(self.L[2 * x + 2], self.L[x], mx - lx)
        l1 = mx - lx - 1 if d > 0 else 0
        l2 = rx - lx - 1 if d > 0 else mx - lx
        self.T[2 * x + 1] = self.op_modify_T(self.T[2 * x + 1], self.L[x], l1)
        self.T[2 * x + 2] = self.op_modify_T(self.T[2 * x + 2], self.L[x], l2)
        self.L[x] = self.NO_OPERATION

    def _update(self, l, r, d, v, x, lx, rx):
        self.propagate(x, lx, rx)
        if l >= rx or lx >= r:
            return
        if lx >= l and rx <= r:
            self.L[x] = self.op_modify_L(self.L[x], (d, v), lx - l)
            l1 = rx - l - 1 if d > 0 else lx - l
            self.T[x] = self.op_modify_T(self.T[x], (d, v), l1)
            return

        mx = (lx + rx) // 2
        self._update(l, r, d, v, 2 * x + 1, lx, mx)
        self._update(l, r, d, v, 2 * x + 2, mx, rx)
        self.T[x] = self.op_query(self.T[2 * x + 1], self.T[2 * x + 2])

    def update(self, l, r, d, v):
        return self._update(l, r, d, v, 0, 0, self.size)

    def first_above_(self, v, x, lx, rx):
        self.propagate(x, lx, rx)
        if self.T[x] < v:
            return -1
        if rx - lx == 1:
            return lx
        mx = (lx + rx) // 2
        res = self.first_above_(v, 2 * x + 1, lx, mx)
        if res == -1:
            res = self.first_above_(v, 2 * x + 2, mx, rx)
        return res

    def first_above(self, v):
        return self.first_above_(v, 0, 0, self.size)

    def _get(self, i, x, lx, rx):
        self.propagate(x, lx, rx)
        if rx - lx == 1:
            return self.T[x]
        mx = (lx + rx) // 2
        if i < mx:
            return self._get(i, 2 * x + 1, lx, mx)
        else:
            return self._get(i, 2 * x + 2, mx, rx)

    def get(self, i):
        return self._get(i, 0, 0, self.size)

import io, os, sys
input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline

if __name__ == '__main__':
    n = int(input())
    STree = SegmentTree(n + 1)

    while True:
        t = input().split()
        if t[0] == "I":
            l, r, d = int(t[1]), int(t[2]), int(t[3])
            v1, v2 = STree.get(l - 1), STree.get(r)
            STree.update(l - 1, r + 1, d, v1)
            v3 = STree.get(r)
            STree.update(r + 1, n + 1, -float("inf"), v3 - v2)

        elif t[0] == "Q":
            x = STree.first_above(int(t[1]) + 1)
            if x == -1:
                print(n)
            else:
                print(x - 1)
        else:
            break