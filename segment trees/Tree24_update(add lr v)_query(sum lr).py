# this segment tree will support two operations:
# 1. apply add with v for all elements on [l, r)
# 2. find sum for all elements on [l, r)
# Now we need to keep length of segment as well for op_modify



class SegmentTree:
    def __init__(self, n, op_modify, op_sum, ZERO):
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.T = [0] * (2 * self.size - 1)   # to multiply
        self.L = [0] * (2 * self.size - 1)   # current sum
        self.op_modify = op_modify
        self.op_sum = op_sum
        self.ZERO = ZERO

    def _build(self, x, lx, rx):
        if rx - lx == 1:
            self.T[x] = 0
            self.L[x] = 0
        else:
            mx = (lx + rx)//2
            self._build(2*x+1, lx, mx)
            self._build(2*x+2, mx, rx)
            self.L[x] = 0
            self.T[x] = self.op_sum(self.T[2*x+1], self.T[2*x+2])

    def build(self):
        self._build(0, 0, self.size)

    def _update(self, l, r, v, x, lx, rx):
        if l >= rx or lx >= r:
            return
        if lx >= l and rx <= r:
            self.L[x] = self.op_modify(self.L[x], v, 1)        # why 1?
            self.T[x] = self.op_modify(self.T[x], v, rx - lx)
            return
        mx = (lx + rx)//2
        self._update(l, r, v, 2*x+1, lx, mx)
        self._update(l, r, v, 2*x+2, mx, rx)
        self.T[x] = self.op_modify(self.op_sum(self.T[2*x+1], self.T[2*x+2]), self.L[x], rx - lx)

    def update(self, l, r, v):
        return self._update(l, r, v, 0, 0, self.size)

    def _query(self, l, r, x, lx, rx):
        if l >= rx or lx >= r:
            return self.ZERO
        if lx >= l and rx <= r:
            return self.T[x]
        mx = (lx + rx) // 2
        m1 = self._query(l, r, 2 * x + 1, lx, mx)
        m2 = self._query(l, r, 2 * x + 2, mx, rx)
        return self.op_modify(self.op_sum(m1, m2), self.L[x], min(rx, r) - max(lx, l))  # careful here!

    def query(self, l, r):
        return self._query(l, r, 0, 0, self.size)

# import io, os, sys
# input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline


if __name__ == '__main__':
    n, m = [int(i) for i in input().split()]
    MOD = 10**9 + 7
    STree = SegmentTree(n, lambda a, b, x: a + b*x, lambda a, b: a+b, 0)
    STree.build()

    for i in range(m):
        t = [int(i) for i in input().split()]
        if t[0] == 1:
            STree.update(t[1], t[2], t[3])
        else:
            print(STree.query(t[1], t[2]))