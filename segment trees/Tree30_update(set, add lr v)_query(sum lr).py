# this segment tree will support two operations:
# TBD


class SegmentTree:
    def __init__(self, n):
        self.size = 1
        while self.size < n:
            self.size *= 2

        self.NO_OPERATION = (-float("inf"), 0)  # it should be neutral with respect to op_modify
        self.ZERO = 0
        self.T = [0] * (2 * self.size - 1)
        self.L = [self.NO_OPERATION] * (2 * self.size - 1)

    def op_modify_L(self, a, b):
        if b[0] != -float("inf"):
            return b
        if b[1] != 0:
            if a[1] != 0: return -float("inf"), a[1] + b[1]
            if a[0] != -float("inf"):
                return a[0] + b[1], 0
        return b

    def op_modify_T(self, x, a, len_):
        if a[0] != -float("inf"): return a[0] * len_
        if a[1] != 0: return x + a[1] * len_
        return x

    def op_sum(self, a, b):
        return a + b

    def propagate(self, x, lx, rx):
        if self.L[x] == self.NO_OPERATION or rx - lx == 1:
            return
        mx = (lx + rx)//2
        self.L[2 * x + 1] = self.op_modify_L(self.L[2 * x + 1], self.L[x])
        self.T[2 * x + 1] = self.op_modify_T(self.T[2 * x + 1], self.L[x], mx - lx)
        self.L[2 * x + 2] = self.op_modify_L(self.L[2 * x + 2], self.L[x])
        self.T[2 * x + 2] = self.op_modify_T(self.T[2 * x + 2], self.L[x], rx - mx)
        self.L[x] = self.NO_OPERATION

    def _update(self, l, r, v, x, lx, rx):
        self.propagate(x, lx, rx)
        if l >= rx or lx >= r:
            return
        if lx >= l and rx <= r:
            self.L[x] = self.op_modify_L(self.L[x], v)
            self.T[x] = self.op_modify_T(self.T[x], v, rx - lx)
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
        if t[0] == 1:
            STree.update(t[1], t[2], (t[3], 0))
        elif t[0] == 2:
            STree.update(t[1], t[2], (-float("inf"), t[3]))
        else:
            print(STree.query(t[1], t[2]))