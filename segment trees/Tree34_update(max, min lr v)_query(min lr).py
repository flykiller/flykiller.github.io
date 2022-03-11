# this segment tree will support two operations:
# 1. apply min or max with value h on interval [r, v)
# 2. find min of elements in interval [r, l)
# For our lazy updates we will keep pairs [h_max, h_min], where
# operation max was applied with h_max and min with h_min. It can be proven
# that we always can keep pairs where h_max <= h_min


class SegmentTree:
    def __init__(self, n):
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.ZERO = float("inf")  # neutral element, for min it is +inf
        self.NO_OPERATION = (1, 0)  # in correct values h[0] always <= h[1]
        self.T = [0] * (2 * self.size - 1)  #   minimums
        self.L = [self.NO_OPERATION] * (2 * self.size - 1)  # lazy updates

    def op_modify_L(self, h0, h1):
        if h0 == self.NO_OPERATION: return h1
        if h1[1] <= h0[0]: return h1[1], h1[1]
        if h0[1] <= h1[0]: return h1[0], h1[0]
        if h1[0] <= h0[0] and h0[1] <= h1[1]: return h0
        if h0[0] <= h1[0] and h1[1] <= h0[1]: return h1
        if h1[0] <= h0[0]: return h0[0], h1[1]
        return h1[0], h0[1]

    def op_modify_T(self, x, h):
        return max(min(x, h[1]), h[0])

    def op_query(self, a, b):
        return min(a, b)

    def propagate(self, x, lx, rx):
        if self.L[x] == self.NO_OPERATION or rx - lx == 1:
            return
        mx = (lx + rx)//2
        self.L[2 * x + 1] = self.op_modify_L(self.L[2 * x + 1], self.L[x])
        self.T[2 * x + 1] = self.op_modify_T(self.T[2 * x + 1], self.L[x])
        self.L[2 * x + 2] = self.op_modify_L(self.L[2 * x + 2], self.L[x])
        self.T[2 * x + 2] = self.op_modify_T(self.T[2 * x + 2], self.L[x])
        self.L[x] = self.NO_OPERATION

    def _update(self, l, r, v, x, lx, rx):
        self.propagate(x, lx, rx)
        if l >= rx or lx >= r:
            return
        if lx >= l and rx <= r:
            self.L[x] = self.op_modify_L(self.L[x], v)
            self.T[x] = self.op_modify_T(self.T[x], v)
            return
        mx = (lx + rx)//2
        self._update(l, r, v, 2*x+1, lx, mx)
        self._update(l, r, v, 2*x+2, mx, rx)
        self.T[x] = self.op_query(self.T[2*x+1], self.T[2*x+2])

    def update(self, l, r, v):
        return self._update(l, r, v, 0, 0, self.size)

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

#import io, os, sys
#input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline


if __name__ == '__main__':
    n, k = [int(i) for i in input().split()]
    STree = SegmentTree(n)

    for i in range(k):
        t = [int(i) for i in input().split()]
        if t[0] == 2:
            STree.update(t[1], t[2] + 1, (-float("inf"), t[3]))
        else:
            STree.update(t[1], t[2] + 1, (t[3], float("inf")))

    print("\n".join([str(STree.get(i)) for i in range(n)]))