# this segment tree will support two operations:
# 1. apply min or max with value h on interval [r, v)
# 2. find min of elements in interval [r, l)
# For our lazy updates we will keep pairs [h_max, h_min], where
# operation max was applied with h_max and min with h_min. It can be proven
# that we always can keep pairs where h_max <= h_min

class SegmentTree:
    def __init__(self, N):
        self.N = N
        self.H = 1
        while 1 << self.H < N:
            self.H += 1
        self.size = 1 << self.H

        self.ZERO = float("inf")  # neutral element, for min it is +inf
        self.NO_OPERATION = (1, 0)  # in correct values h[0] always <= h[1]
        self.T = [0] * (2 * self.size - 1)  # minimums
        self.L = [self.NO_OPERATION] * (2 * self.size - 1)  # lazy updates

    def op_modify_L(self, h0, h1):
        if h0 == self.NO_OPERATION: return h1
        if h1 == self.NO_OPERATION: return h0
        if h1[1] <= h0[0]: return h1[1], h1[1]
        if h0[1] <= h1[0]: return h1[0], h1[0]
        if h1[0] <= h0[0] and h0[1] <= h1[1]: return h0
        if h0[0] <= h1[0] and h1[1] <= h0[1]: return h1
        if h1[0] <= h0[0]: return h0[0], h1[1]
        return h1[0], h0[1]

    def op_modify_T(self, x, h):
        if h == self.NO_OPERATION: return x
        return max(min(x, h[1]), h[0])

    def op_query(self, a, b):
        return min(a, b)

    def _apply(self, x, val):
        self.T[x] = self.op_modify_T(self.T[x], val)
        self.L[x] = self.op_modify_L(self.L[x], val)

    def _pull(self, x):
        while x > 1:
            x //= 2
            self.T[x] = self.op_query(self.T[x*2], self.T[x*2 + 1])
            self.T[x] = self.op_modify_T(self.T[x], self.L[x])

    def _push(self, x):
        for h in range(self.H, 0, -1):
            y = x >> h
            if self.L[y] != self.NO_OPERATION:
                self._apply(y * 2, self.L[y])
                self._apply(y * 2 + 1, self.L[y])
                self.L[y] = self.NO_OPERATION

    def update(self, l, r, h):
        l += self.N
        r += self.N
        self._push(l)
        self._push(r)
        l0, r0 = l, r
        while l <= r:
            if l & 1:
                self._apply(l, h)
                l += 1
            if r & 1 == 0:
                self._apply(r, h)
                r -= 1
            l //= 2; r //= 2
        self._pull(l0)
        self._pull(r0)

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