# this segment tree will support two operations:
# 1. add value v to all elements in [l, r)
# 2. answer query: find the first element with index >= l such that it is >= x
# Let us use Segment Tree 07, but with massive operations now:
# 1. add value v to all elements in [l, r)
# 2. find maximum in [l, r)


class SegmentTree:
    def __init__(self, n):
        self.size = 1
        while self.size < n:
            self.size *= 2

        self.NO_OPERATION = (0, 0)  # it should be neutral with respect to op_modify
        self.ZERO = 0
        self.T = [0] * (2 * self.size - 1)
        self.L = [self.NO_OPERATION] * (2 * self.size - 1)

    def op_sum(self, a, b):
        return a + b

    def propagate(self, x, lx, rx):
        if self.L[x] == self.NO_OPERATION or rx - lx == 1:
            return
        mx = (lx + rx)//2
        a, d = self.L[x]
        a1, d1 = self.L[2 * x + 1]
        a2, d2 = self.L[2 * x + 2]
        self.L[2 * x + 1] = a + a1, d + d1
        self.L[2 * x + 2] = a + d * (mx - lx) + a2, d + d2
        self.T[2 * x + 1] += (2 * a + d*(mx - lx - 1)) * (mx - lx)//2
        self.T[2 * x + 2] += (2 * a + d*(mx + rx - 2*lx - 1)) * (rx - mx)//2
        self.L[x] = self.NO_OPERATION

    def _update(self, l, r, a, d, x, lx, rx):
        self.propagate(x, lx, rx)
        if l >= rx or lx >= r:
            return
        if lx >= l and rx <= r:
            # print("!!!!", lx, rx, l, r)
            a1, d1 = self.L[x]
            a2, d2 = a + (lx - l) * d, d
            self.L[x] = a1 + a2, d1 + d2
            self.T[x] += (2 * a2 + d2 * (rx - lx - 1)) * (rx - lx)//2
            return
        mx = (lx + rx)//2
        self._update(l, r, a, d, 2*x+1, lx, mx)
        self._update(l, r, a, d, 2*x+2, mx, rx)
        self.T[x] = self.op_sum(self.T[2*x+1], self.T[2*x+2])

    def update(self, l, r, a, d):
        return self._update(l, r, a, d, 0, 0, self.size)

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
        if t[0] == 1:
            STree.update(t[1]-1, t[2], t[3], t[4])
            #print(t[1] - 1, t[2], t[3], t[4])
            #print("!!!", STree.T)
            #print("@@@", STree.L)
        elif t[0] == 2:

            print(STree.query(t[1]-1, t[1]))