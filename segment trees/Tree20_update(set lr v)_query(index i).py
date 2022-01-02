# this segment tree will support two operations:
# 1. For all elements in range [r, l) apply ai = v. This operation is associative  f(a,x) = a, but not commutative,
# so we need to use push technique here. Also for each node we need to have information if we need to apply
# operation or not, because 0 is not good choice.
# 2. Find element at index i

class SegmentTree:
    def __init__(self, n, arr, NO_OPERATION):
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.T = [0] * (2 * self.size - 1)
        self.NO_OP = NO_OPERATION
        self.arr = arr

    def propagate(self, x, lx, rx):
        if self.T[x] == self.NO_OP or rx - lx == 1:
            return
        self.T[2*x+1] = self.T[x]
        self.T[2*x+2] = self.T[x]
        self.T[x] = self.NO_OP

    def _modify(self, l, r, v, x, lx, rx):
        self.propagate(x, lx, rx)
        if l >= rx or lx >= r:
            return
        if lx >= l and rx <= r:
            self.T[x] = v
            return
        mx = (lx + rx)//2
        self._modify(l, r, v, 2*x+1, lx, mx)
        self._modify(l, r, v, 2*x+2, mx, rx)

    def modify(self, l, r, v):
        return self._modify(l, r, v, 0, 0, self.size)

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

# import io, os, sys
# input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline


if __name__ == '__main__':
    n, m = [int(i) for i in input().split()]
    STree = SegmentTree(n, [0]*n, -float("inf"))

    for i in range(m):
        t = [int(i) for i in input().split()]
        if t[0] == 1:
            STree.modify(t[1], t[2], t[3])
        else:
            print(STree.get(t[1]))