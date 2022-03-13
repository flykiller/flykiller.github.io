# this segment tree will support two operations:
# 1. set values in range [l, r) as arithmetic progression with parameters a, d or
# add value v to value in this range.
# 2. find maximum in range [l, r)

# In lazy updates we will keep pair (d, v) where d means that we need to set values to
# 0, d, 2d, ... and v means that after we add v to all values.
# If d = -inf, it means that we skip the first step.

from collections import defaultdict

from collections import defaultdict


class SegmentTree:
    def __init__(self, n):
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.ZERO = -float("inf")  # neutral element, for ma it is +inf
        self.NO_OPERATION = (float("inf"), 0)
        self.T = defaultdict(int)
        self.L = defaultdict(lambda: self.NO_OPERATION)

    def op_query(self, a, b):
        return max(a, b)

    def op_modify_L(self, h0, h1, len_):
        d, v = h1
        if d != -float("inf"):
            return d, v + d * len_
        else:
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

    def propagate(self, x, lx, rx):

        if self.L[x] == self.NO_OPERATION or rx - lx == 1:
            return
        print("!!!!", lx, rx)
        mx = (lx + rx) // 2
        d, v = self.L[x]
        self.L[2 * x + 1] = self.op_modify_L(self.L[2 * x + 1], self.L[x], 0)
        self.L[2 * x + 2] = self.op_modify_L(self.L[2 * x + 2], self.L[x], K1[mx] - K1[lx])
        l1 = K1[mx] - K1[lx] - 1 if d > 0 else 0
        l2 = K1[rx] - K1[lx] - 1 if d > 0 else K1[mx] - K1[lx]
        self.T[2 * x + 1] = self.op_modify_T(self.T[2 * x + 1], self.L[x], l1)
        self.T[2 * x + 2] = self.op_modify_T(self.T[2 * x + 2], self.L[x], l2)
        self.L[x] = self.NO_OPERATION

    def _update(self, l, r, d, v, x, lx, rx):

        self.propagate(x, lx, rx)
        if l >= rx or lx >= r:
            return
        if lx >= l and rx <= r:
            print(l, r, lx, rx)
            self.L[x] = self.op_modify_L(self.L[x], (d, v), K1[lx] - K1[l])
            l1 = K1[rx] - K1[l] - 1 if d > 0 else K1[lx] - K1[l]
            self.T[x] = self.op_modify_T(self.T[x], (d, v), l1)
            return

        mx = (lx + rx) // 2
        self._update(l, r, d, v, 2 * x + 1, lx, mx)
        self._update(l, r, d, v, 2 * x + 2, mx, rx)
        self.T[x] = self.op_query(self.T[2 * x + 1], self.T[2 * x + 2])

    def update(self, l, r, d, v):
        return self._update(l, r, d, v, 0, 0, self.size)

    def first_above_(self, v, x, lx, rx):
        self.propagate(x, lx, rx)
        if self.T[x] < v:
            return -1
        if rx - lx == 1:
            return lx
        mx = (lx + rx) // 2
        res = self.first_above_(v, 2 * x + 1, lx, mx)
        if res == -1:
            res = self.first_above_(v, 2 * x + 2, mx, rx)
        return res

    def first_above(self, v):
        return self.first_above_(v, 0, 0, self.size)

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
    n = int(input())
    STree = SegmentTree(n + 1)
    arr = []
    idxs = set([n + 1])

    while True:
        t = input().split()
        if t[0] == "I":
            l, r, d = int(t[1]), int(t[2]), int(t[3])
            arr += [[1, l, r, d]]
            idxs.add(l-1)
            idxs.add(l)
            idxs.add(r)
            idxs.add(r + 1)
        elif t[0] == "Q":
            arr += [[0, int(t[1]) + 1]]
        else:
            break

    K1 = sorted(list(idxs))
    K2 = {x: i for i, x in enumerate(K1)}
    print(K1, K2)

    for line in arr:
        if line[0] == 1:
            l, r, d = line[1], line[2], line[3]
            v1, v2 = STree.get(K2[l - 1]), STree.get(K2[r])
            #print(l, r, K2[l - 1], K2[r + 1])
            STree.update(K2[l - 1], K2[r + 1], d, (K1[K2[l-1]] - K1[K2[l]] + 1) * d + v1)
            v3 = STree.get(K2[r])
            STree.update(K2[r + 1], K2[n + 1], -float("inf"), v3 - v2)
            print([STree.get(i) for i in range(n + 1)])