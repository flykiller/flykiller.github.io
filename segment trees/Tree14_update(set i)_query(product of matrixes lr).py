# this segment tree will support two operations:
# 1. Set element i equal to v.
# 2. Find product of matrices in range [l, r]
# In segment we will keep product of matrices in this segment

class SegmentTree:
    def __init__(self, n, arr, ZERO):
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.T = [ZERO] * (2 * self.size - 1)
        self.arr = arr
        self.ZERO = ZERO

    def mult(self, A, B):
        C = (A[0] * B[0] + A[1] * B[2], A[0] * B[1] + A[1] * B[3], A[2] * B[0] + A[3] * B[2], A[2] * B[1] + A[3] * B[3])
        return C[0] % r, C[1] % r, C[2] % r, C[3] % r

    def _build(self, x, lx, rx):
        if rx - lx == 1:
            if lx < len(self.arr):
                self.T[x] = self.arr[lx]
        else:
            mx = (lx + rx) // 2
            self._build(2 * x + 1, lx, mx)
            self._build(2 * x + 2, mx, rx)
            self.T[x] = self.mult(self.T[2 * x + 1], self.T[2 * x + 2])

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
        self.T[x] = self.mult(self.T[2 * x + 1], self.T[2 * x + 2])

    def set(self, i, v):
        self._set(i, v, 0, 0, self.size)

    def _prod(self, l, r, x, lx, rx):
        if l >= rx or lx >= r:
            return self.ZERO
        if lx >= l and rx <= r:
            return self.T[x]
        mx = (lx + rx) // 2
        s1 = self._prod(l, r, 2 * x + 1, lx, mx)
        s2 = self._prod(l, r, 2 * x + 2, mx, rx)
        return self.mult(s1, s2)

    def prod(self, l, r):
        return self._prod(l, r, 0, 0, self.size)


# import io, os, sys
# input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline

if __name__ == '__main__':
    r, n, m = [int(i) for i in input().split()]
    arr = []
    for _ in range(n):
        a, b = [int(i) for i in input().split()]
        c, d = [int(i) for i in input().split()]
        _ = input()
        arr += [[a, b, c, d]]
    STree = SegmentTree(n, arr, (1, 0, 0, 1))
    STree.build()

    for i in range(m):
        i, j = [int(i) for i in input().split()]
        a, b, c, d = STree.prod(i - 1, j)
        print(str(a) + " " + str(b) + "\n" + str(c) + " " + str(d) + "\n")
