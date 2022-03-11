# this segment tree will support two operations:
# 1. Add v to range [r, l)
# 2. Get element in index i
# The idea is to keep array of differences, so original array is cumulative sums.
# To change array of differences we just need to change two elements: add v to l-th and subtract v from r-th
# We use Segment Tree 01

class SegmentTree:
    def __init__(self, n, arr):
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.T = [0] * (2 * self.size - 1)
        self.arr = arr

    def _build(self, x, lx, rx):
        if rx - lx == 1:
            if lx < len(self.arr):
                self.T[x] = self.arr[lx]
        else:
            mx = (lx + rx) // 2
            self._build(2 * x + 1, lx, mx)
            self._build(2 * x + 2, mx, rx)
            self.T[x] = self.T[2 * x + 1] + self.T[2 * x + 2]

    def build(self):
        self._build(0, 0, self.size)

    def _set(self, i, v, x, lx, rx):
        if rx - lx == 1:
            self.T[x] = v
            return
        mx = (lx + rx) // 2
        if i < mx:
            self._set(i, v, 2 * x + 1, lx, mx)
        else:
            self._set(i, v, 2 * x + 2, mx, rx)
        self.T[x] = self.T[2 * x + 1] + self.T[2 * x + 2]

    def set(self, i, v):
        self._set(i, v, 0, 0, self.size)

    def _sum(self, l, r, x, lx, rx):
        if l >= rx or lx >= r:
            return 0
        if lx >= l and rx <= r:
            return self.T[x]
        mx = (lx + rx) // 2
        s1 = self._sum(l, r, 2 * x + 1, lx, mx)
        s2 = self._sum(l, r, 2 * x + 2, mx, rx)
        return s1 + s2

    def sum(self, l, r):
        return self._sum(l, r, 0, 0, self.size)


# import io, os, sys
# input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline

if __name__ == '__main__':
    n, m = [int(i) for i in input().split()]
    STree = SegmentTree(n + 1, [0] * (n + 1))
    STree.build()

    for i in range(m):
        t = [int(i) for i in input().split()]
        if t[0] == 1:
            l, r, v = t[1], t[2], t[3]
            A, B = STree.sum(l, l + 1), STree.sum(r, r + 1)
            STree.set(l, A + v)
            STree.set(r, B - v)
        else:
            print(STree.sum(0, t[1] + 1))
