# this is problem, is opposite to previous, given answer, return permutation.
# the idea is to use Segment Tree 05 where we need to find k-th one.
# Imagine, that we have [4 1 3 5 2] then in the beginning we have
# [1 1 1 1 1] -> [1 0 1 1 1] -> [1 0 1 1 0] -> ...

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

    def find_k_(self, k, x, lx, rx):
        if rx - lx == 1:
            return lx
        mx = (lx + rx)//2
        if k < self.T[2*x+1]:
            return self.find_k_(k, 2*x+1, lx, mx)
        else:
            return self.find_k_(k - self.T[2*x+1], 2*x+2, mx, rx)

    def find_k(self, k):
        return self.find_k_(k, 0, 0, self.size)

#import io, os, sys
#input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline

if __name__ == '__main__':
    n = int(input())
    arr = [int(i) for i in input().split()][::-1]
    ans = []
    STree = SegmentTree(n, [1]*n)
    STree.build()
    for num in arr:
        k = STree.find_k(num)
        STree.set(k, 0)
        ans += [n-k]

    print(" ".join(str(x) for x in ans[::-1]))
