# this segment tree will support two operations:
# 1. apply set with value v for all elements on [l, r)
# 2. find subarray with maximum sum
# Let us use Segment Tree 04, but with massive operations now.


class SegmentTree:
    def __init__(self, n):
        self.size = 1
        while self.size < n:
            self.size *= 2

        self.ZERO = (0, 0, 0, 0)  # neutral element, for min it is +inf
        self.NO_OPERATION = -float("inf")  # this is for our propagate to understand that we do not need it
        self.T = [self.ZERO] * (2 * self.size - 1)
        self.L = [0] * (2 * self.size - 1)

    def op_modify(self, a, b, len_):
        if b == self.NO_OPERATION:
            return a
        return max(0, b * len_), max(0, b * len_), max(0, b * len_), b * len_

    def op_sum(self, a, b):
        return max(a[0], b[0], a[2] + b[1]), max(a[1], a[3] + b[1]), max(b[2], b[3] + a[2]), a[3] + b[3]

    def propagate(self, x, lx, rx):
        if self.L[x] == self.NO_OPERATION or rx - lx == 1:
            return
        mx = (lx + rx)//2
        self.L[2 * x + 1] = self.L[x]
        self.T[2 * x + 1] = self.op_modify(self.T[2 * x + 1], self.L[x], mx - lx)
        self.L[2 * x + 2] = self.L[x]
        self.T[2 * x + 2] = self.op_modify(self.T[2 * x + 2], self.L[x], rx - mx)
        self.L[x] = self.NO_OPERATION

    def _update(self, l, r, v, x, lx, rx):
        self.propagate(x, lx, rx)
        if l >= rx or lx >= r:
            return
        if lx >= l and rx <= r:
            self.L[x] = v        # why 1?
            self.T[x] = self.op_modify(self.T[x], v, rx - lx)
            return
        mx = (lx + rx)//2
        self._update(l, r, v, 2*x+1, lx, mx)
        self._update(l, r, v, 2*x+2, mx, rx)
        self.T[x] = self.op_sum(self.T[2*x+1], self.T[2*x+2])

    def update(self, l, r, v):
        return self._update(l, r, v, 0, 0, self.size)

    def _query(self, l, r, x, lx, rx):
        self.propagate(x, lx, rx)
        if l >= rx or lx >= r:
            return self.ZERO
        if lx >= l and rx <= r:
            return self.T[x]
        mx = (lx + rx) // 2
        m1 = self._query(l, r, 2 * x + 1, lx, mx)
        m2 = self._query(l, r, 2 * x + 2, mx, rx)
        return self.op_sum(m1, m2)

    def query(self, l, r):
        return self._query(l, r, 0, 0, self.size)

# import io, os, sys
# input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline


if __name__ == '__main__':
    n, m = [int(i) for i in input().split()]
    MOD = 10**9 + 7
    STree = SegmentTree(n)

    for i in range(m):
        t = [int(i) for i in input().split()]
        STree.update(t[0], t[1], t[2])
        print(STree.T[0][0])