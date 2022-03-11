# this segment tree will support two operations:
# 1. Set element i equal to v.
# 2. Find number of minimum elements in range [r, l)


class SegmentTree:
    def __init__(self, n, arr, ZERO):
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.T = [(0, 0)] * (2 * self.size - 1)   # now we keep pair (min, count of min)
        self.arr = arr
        self.ZERO = ZERO       #neutral element

    def combine(self, a, b):
        if a[0] < b[0]: return a
        if a[0] > b[0]: return b
        return a[0], a[1] + b[1]

    def _build(self, x, lx, rx):
        if rx - lx == 1:
            if lx < len(self.arr):
                self.T[x] = (self.arr[lx], 1)   # fill list with frequency 1
        else:
            mx = (lx + rx)//2
            self._build(2*x+1, lx, mx)
            self._build(2*x+2, mx, rx)
            self.T[x] = self.combine(self.T[2*x+1], self.T[2*x+2])

    def build(self):
        self._build(0, 0, self.size)

    def _set(self, i, v, x, lx, rx):
        if rx - lx == 1:
            self.T[x] = (v, 1)  # fill with frequency 1
            return
        mx = (lx + rx) // 2
        if i < mx:
            self._set(i, v, 2 * x + 1, lx, mx)
        else:
            self._set(i, v, 2 * x + 2, mx, rx)
        self.T[x] = self.combine(self.T[2 * x + 1], self.T[2 * x + 2])

    def set(self, i, v):
        self._set(i, v, 0, 0, self.size)

    def _calc(self, l, r, x, lx, rx):
        if l >= rx or lx >= r:
            return self.ZERO
        if lx >= l and rx <= r:
            return self.T[x]
        mx = (lx + rx) // 2
        s1 = self._calc(l, r, 2 * x + 1, lx, mx)
        s2 = self._calc(l, r, 2 * x + 2, mx, rx)
        return self.combine(s1, s2)

    def calc(self, l, r):
        return self._calc(l, r, 0, 0, self.size)


if __name__ == '__main__':
    n, m = [int(i) for i in input().split()]
    arr = [int(i) for i in input().split()]
    STree = SegmentTree(n, arr, (float("inf"), 0))
    STree.build()

    for i in range(m):
        t = [int(i) for i in input().split()]
        if t[0] == 1:
            STree.set(t[1], t[2])
        else:
            x, y = STree.calc(t[1], t[2])
            print(str(x) + " " + str(y))