# Given permutation find number of inversions for each index
# The idea is to use segment tree with two operations:
# 1. set element in index i equal to v
# 2. evaluate sum of elements in suffix.
# So we will use segment tree 01 we have.
# imagine that we have [4, 1, 3, 5, 2], then we add element by element :
# [0, 0, 0, 0, 0] -> [0, 0, 0, 1, 0] -> [0, 1, 0, 0, 1] and so on

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

#import io, os, sys
#input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline

if __name__ == '__main__':
    n = int(input())
    arr = [int(i) for i in input().split()]
    ans = []
    STree = SegmentTree(n, [0]*n)
    STree.build()
    for num in arr:
        ans += [STree.sum(num, n)]
        STree.set(num-1, 1)

    print(" ".join(str(x) for x in ans))
