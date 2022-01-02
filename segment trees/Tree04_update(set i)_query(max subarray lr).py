# this segment tree will support two operations:
# 1. Set element i equal to v.
# 2. Find maximum sum of subarray of
# original array (in fact we can answer this question for all subarrays, not only for original one) we will keep
# tuple (seg, pref, suf, sum) for each node
# use fast IO to get AC on PyPy27


class SegmentTree:
    def __init__(self, n, arr, ZERO):
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.T = [ZERO] * (2 * self.size - 1)  # now we keep pair (min, count of min)
        self.arr = arr
        self.ZERO = ZERO  # neutral element

    def combine(self, a, b):
        return max(a[0], b[0], a[2] + b[1]), max(a[1], a[3] + b[1]), max(b[2], b[3] + a[2]), a[3] + b[3]

    def one_element(self, x):
        return max(x, 0), max(x, 0), max(x, 0), x

    def _build(self, x, lx, rx):
        if rx - lx == 1:
            if lx < len(self.arr):
                self.T[x] = self.one_element(self.arr[lx])  # segment with one element
        else:
            mx = (lx + rx) // 2
            self._build(2 * x + 1, lx, mx)
            self._build(2 * x + 2, mx, rx)
            self.T[x] = self.combine(self.T[2 * x + 1], self.T[2 * x + 2])

    def build(self):
        self._build(0, 0, self.size)

    def _set(self, i, v, x, lx, rx):
        if rx - lx == 1:
            self.T[x] = self.one_element(v)
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
    STree = SegmentTree(n, arr, (0, 0, 0, 0))
    STree.build()
    print(STree.T[0][0])  # we can make calc instead

    for i in range(m):
        t = [int(i) for i in input().split()]
        STree.set(t[0], t[1])
        print(STree.T[0][0])  # we can make calc instead
