# this segment tree will support two operations:
# 1. add value d to segment [r, l)
# 2. For segment [r, l) find weighted sum: A[r]*1 + A[r+1]*2 + ...
# we will keep in T two values (sum, weighted sum)
# we will keep in L one value lazy update: d
# now what we need to understand is how to propagate updates.


class SegmentTree:
    def __init__(self, n):
        self.size = 1
        while self.size < n:
            self.size *= 2

        self.NO_OPERATION = 0  # it should be neutral with respect to op_modify
        self.ZERO = (-float("inf"), -float("inf"))
        self.T = [(0, 0)] * (2 * self.size - 1)
        self.L = [self.NO_OPERATION] * (2 * self.size - 1)

    def op_sum(self, a, b, len_):
        if a == self.ZERO: return b   # this is subtle moment: we need to make sure that function
        if b == self.ZERO: return a   # with zero element is zero
        return a[0] + b[0], a[1] + b[1] + len_ * b[0]

    def propagate(self, x, lx, rx):
        if self.L[x] == self.NO_OPERATION or rx - lx == 1:
            return
        mx = (lx + rx)//2
        self.L[2 * x + 1] += self.L[x]
        self.L[2 * x + 2] += self.L[x]
        s1, w1 = self.T[2 * x + 1]
        s2, w2 = self.T[2 * x + 2]
        l1, l2 = mx - lx, rx - mx
        self.T[2 * x + 1] = s1 + self.L[x] * l1, w1 + self.L[x] * (l1 + 1) * l1 // 2
        self.T[2 * x + 2] = s2 + self.L[x] * l2, w2 + self.L[x] * (l2 + 1) * l2 // 2
        self.L[x] = self.NO_OPERATION

    def _update(self, l, r, d, x, lx, rx):
        self.propagate(x, lx, rx)
        if l >= rx or lx >= r:
            return
        if lx >= l and rx <= r:
            self.L[x] += d
            s, w = self.T[x]
            ll = rx - lx
            self.T[x] = s + d * ll, w + d * ll * (ll + 1) // 2
            return
        mx = (lx + rx)//2
        self._update(l, r, d, 2*x+1, lx, mx)
        self._update(l, r, d, 2*x+2, mx, rx)
        self.T[x] = self.op_sum(self.T[2*x+1], self.T[2*x+2], mx - lx)

    def update(self, l, r, d):
        return self._update(l, r, d, 0, 0, self.size)

    def _query(self, l, r, x, lx, rx):
        self.propagate(x, lx, rx)
        if l >= rx or lx >= r:
            return self.ZERO
        if lx >= l and rx <= r:
            return self.T[x]
        mx = (lx + rx) // 2
        m1 = self._query(l, r, 2 * x + 1, lx, mx)
        m2 = self._query(l, r, 2 * x + 2, mx, rx)
        return self.op_sum(m1, m2, mx - max(lx, l))  # careful here, I spend 2 hours to find it

    def query(self, l, r):
        return self._query(l, r, 0, 0, self.size)


import io, os, sys
input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline

if __name__ == '__main__':
    n, m = [int(i) for i in input().split()]
    STree = SegmentTree(n)
    arr = [int(i) for i in input().split()]
    for i in range(n):
        STree.update(i, i+1, arr[i])  # not optimal way

    for i in range(m):
        t = [int(i) for i in input().split()]
        if t[0] == 1:
            STree.update(t[1] - 1, t[2], t[3])
        else:
            s, w = STree.query(t[1] - 1, t[2])
            print(w)