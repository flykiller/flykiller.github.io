# The idea is the following: go from the left to the right and
# 1) if we meet start of segment, save it
# 2) if we meet end of segment, set start of this segment as 1 and calculate number of ones inside
# so we use Segment Tree 01

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
            mx = (lx + rx)//2
            self._build(2*x+1, lx, mx)
            self._build(2*x+2, mx, rx)
            self.T[x] = self.T[2*x+1] + self.T[2*x+2]

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
# input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline


if __name__ == '__main__':
    n = int(input())
    arr = [int(i) for i in input().split()]
    ans = [0]*n
    d = {}
    STree = SegmentTree(2*n, [0]*(2*n))
    STree.build()
    for i, num in enumerate(arr):
        if num not in d:
            d[num] = i
        else:
            start = d[num]
            ans[num-1] = STree.sum(start+1, i)
            STree.set(start, 1)

    print(" ".join(str(x) for x in ans))
