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

        self.NO_OPERATION = 0  # it should be neutral with respect to op_modify
        self.T = [0] * (2 * self.size - 1)
        self.L = [0] * (2 * self.size - 1)

    def op_modify(self, a, b):
        return a + b

    def op_sum(self, a, b):
        return max(a, b)

    def propagate(self, x, lx, rx):
        if self.L[x] == self.NO_OPERATION or rx - lx == 1:
            return
        mx = (lx + rx)//2
        self.L[2 * x + 1] = self.op_modify(self.L[2 * x + 1], self.L[x])
        self.T[2 * x + 1] = self.op_modify(self.T[2 * x + 1], self.L[x])
        self.L[2 * x + 2] = self.op_modify(self.L[2 * x + 2], self.L[x])
        self.T[2 * x + 2] = self.op_modify(self.T[2 * x + 2], self.L[x])
        self.L[x] = self.NO_OPERATION

    def _update(self, l, r, v, x, lx, rx):
        self.propagate(x, lx, rx)
        if l >= rx or lx >= r:
            return
        if lx >= l and rx <= r:
            self.L[x] = self.op_modify(self.L[x], v)
            self.T[x] = self.op_modify(self.T[x], v)
            return
        mx = (lx + rx)//2
        self._update(l, r, v, 2*x+1, lx, mx)
        self._update(l, r, v, 2*x+2, mx, rx)
        self.T[x] = self.op_sum(self.T[2*x+1], self.T[2*x+2])

    def update(self, l, r, v):
        return self._update(l, r, v, 0, 0, self.size)

    def first_above_(self, v, l, x, lx, rx):
        self.propagate(x, lx, rx)
        if self.T[x] < v or rx <= l:
            return -1
        if rx - lx == 1:
            return lx
        mx = (lx + rx) // 2
        res = self.first_above_(v, l, 2 * x + 1, lx, mx)
        if res == -1:
            res = self.first_above_(v, l, 2 * x + 2, mx, rx)
        return res

    def first_above(self, v, l):
        return self.first_above_(v, l, 0, 0, self.size)

# import io, os, sys
# input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline


if __name__ == '__main__':
    n, m = [int(i) for i in input().split()]
    MOD = 10**9 + 7
    STree = SegmentTree(n)

    for i in range(m):
        t = [int(i) for i in input().split()]
        if t[0] == 1:
            STree.update(t[1], t[2], t[3])
            #print("!!!", STree.L, STree.T)
        else:
            print(STree.first_above(t[1], t[2]))