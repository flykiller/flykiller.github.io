# this segment tree will support two operations:
# 1. Set element i equal to v.
# 2. Find k-th one in our array, indexing start with 0, that is we can ask for 0-th one.
# Idea is to start with tree root and each time choose direction

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

if __name__ == '__main__':
    n, m = [int(i) for i in input().split()]
    arr = [int(i) for i in input().split()]
    STree = SegmentTree(n, arr)
    STree.build()

    for i in range(m):
        t = [int(i) for i in input().split()]
        if t[0] == 1:
            arr[t[1]] = 1 - arr[t[1]]
            STree.set(t[1], arr[t[1]])
        else:
            print(STree.find_k(t[1]))