# not finished, I am not sure how to do iterative version for lengths

from collections import defaultdict


class SegmentTree:
    def __init__(self, N):
        self.N = N
        self.H = 1
        while 1 << self.H < N:
            self.H += 1
        self.size = 1 << self.H

        self.ZERO = -float("inf")  # neutral element, for ma it is +inf
        self.NO_OPERATION = (float("inf"), 0)
        self.T = defaultdict(int)
        self.L = defaultdict(lambda: self.NO_OPERATION)

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

    def op_query(self, a, b):
        return max(a, b)

    def _apply(self, x, val):
        self.T[x] = self.op_modify_T(self.T[x], val)
        self.L[x] = self.op_modify_L(self.L[x], val)

    def _pull(self, x):
        while x > 1:
            x //= 2
            self.T[x] = self.op_query(self.T[x*2], self.T[x*2 + 1])
            self.T[x] = self.op_modify_T(self.T[x], self.L[x])

    def _push(self, x):                     # it is like propagate, we need also coodrinates
        for h in range(self.H, 0, -1):
            y = x >> h
            if self.L[y] != self.NO_OPERATION:
                self._apply(y * 2, self.L[y])
                self._apply(y * 2 + 1, self.L[y])

                self.L[y] = self.NO_OPERATION

    def update(self, lx, rx, d, v):
        lx += self.N
        rx += self.N
        self._push(lx)
        self._push(rx)
        l, r = lx, rx
        while lx <= rx:
            if lx & 1:
                l1 = rx - l - 1 if d > 0 else lx - l
                self.T[lx] = self.op_modify_T(self.T[lx], (d, v), l1)
                self.L[lx] = self.op_modify_L(self.L[lx], (d, v), lx - l)
                lx += 1
            if rx & 1 == 0:
                l1 = rx - l - 1 if d > 0 else lx - l
                self.T[rx] = self.op_modify_T(self.T[rx], (d, v), l1)
                self.L[rx] = self.op_modify_L(self.L[rx], (d, v), lx - l)
                rx -= 1
            lx //= 2; rx //= 2
        self._pull(l)
        self._pull(r)

    def query(self, l, r):
        l += self.N
        r += self.N
        self._push(l); self._push(r)
        ans = self.ZERO
        while l <= r:
            if l & 1:
                ans = self.op_query(ans, self.T[l])
                l += 1
            if r & 1 == 0:
                ans = self.op_query(ans, self.T[r])
                r -= 1
            l //= 2; r //= 2
        return ans

# import io, os, sys
# input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline


if __name__ == '__main__':
    n, k = [int(i) for i in input().split()]
    STree = SegmentTree(n)
    sh = 0

    for i in range(k):
        t = [int(i) for i in input().split()]
        if t[0] == 2:
            STree.update(t[1]+sh, t[2]+sh, (-float("inf"), t[3]))
        else:
            STree.update(t[1]+sh, t[2]+sh, (t[3], float("inf")))

    print("\n".join([str(STree.query(i, i)) for i in range(n)]))