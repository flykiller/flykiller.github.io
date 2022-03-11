# this segment tree will support two operations:
# 1. Add value v to elements in range [r, l)
# 2. Find element at index i

class SegmentTree:
    def __init__(self, n, arr):
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.T = [0] * (2 * self.size - 1)
        self.arr = arr

    def _add(self, l, r, v, x, lx, rx):
        if l >= rx or lx >= r:
            return
        if lx >= l and rx <= r:
            self.T[x] += v
            return
        mx = (lx + rx)//2
        self._add(l, r, v, 2*x+1, lx, mx)
        self._add(l, r, v, 2*x+2, mx, rx)

    def add(self, l, r, v):
        return self._add(l, r, v, 0, 0, self.size)

    def _get(self, i, x, lx, rx):
        if rx - lx == 1:
            return self.T[x]
        mx = (lx + rx) // 2
        if i < mx:
            return self._get(i, 2 * x + 1, lx, mx) + self.T[x]
        else:
            return self._get(i, 2 * x + 2, mx, rx) + self.T[x]

    def get(self, i):
        return self._get(i, 0, 0, self.size)

#import io, os, sys
#input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline


if __name__ == '__main__':
    n, m = [int(i) for i in input().split()]
    STree = SegmentTree(n, [0]*n)

    for i in range(m):
        t = [int(i) for i in input().split()]
        if t[0] == 1:
            STree.add(t[1], t[2], t[3])
        else:
            print(STree.get(t[1]))