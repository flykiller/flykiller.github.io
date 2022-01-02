# this segment tree will support two operations:
# 1. add value v to all elements in range [l, r)
# 2. find min for all elements in range [l, r)
# now in tree we keep two values: what we need to add and current min
# here we do not use propagation, because operations are commutative


class SegmentTree:
    def __init__(self, n, arr):
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.T = [0] * (2 * self.size - 1)   # to add
        self.L = [0] * (2 * self.size - 1)   # current min
        self.arr = arr

    def _add(self, l, r, v, x, lx, rx):
        if l >= rx or lx >= r:
            return
        if lx >= l and rx <= r:
            self.T[x] += v
            self.L[x] += v
            return
        mx = (lx + rx)//2
        self._add(l, r, v, 2*x+1, lx, mx)
        self._add(l, r, v, 2*x+2, mx, rx)
        self.T[x] = min(self.T[2*x+1], self.T[2*x+2]) + self.L[x]

    def add(self, l, r, v):
        return self._add(l, r, v, 0, 0, self.size)

    def _min(self, l, r, x, lx, rx):
        if l >= rx or lx >= r:
            return float("inf")
        if lx >= l and rx <= r:
            return self.T[x]
        mx = (lx + rx) // 2
        m1 = self._min(l, r, 2 * x + 1, lx, mx)
        m2 = self._min(l, r, 2 * x + 2, mx, rx)
        return min(m1, m2) + self.L[x]

    def min(self, l, r):
        return self._min(l, r, 0, 0, self.size)

# import io, os, sys
# input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline


if __name__ == '__main__':
    n, m = [int(i) for i in input().split()]
    STree = SegmentTree(n, [0]*n)

    for i in range(m):
        t = [int(i) for i in input().split()]
        if t[0] == 1:
            STree.add(t[1], t[2], t[3])
        else:
            print(STree.min(t[1], t[2]))