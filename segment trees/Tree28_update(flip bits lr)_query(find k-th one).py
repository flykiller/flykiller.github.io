class SegmentTree:
    def __init__(self, n):
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.T = [0] * (2 * self.size - 1)  # keep sums
        self.L = [0] * (2 * self.size - 1)  # for each node 1 if we need to flip
        self.ZERO = 0  # neutral element, for min it is +inf
        self.NO_OPERATION = 0  # this is for our propagate to understand that we do not need it

    def op_modify(self, a, len_):
        return len_ - a

    def op_sum(self, a, b):
        return a + b

    def propagate(self, x, lx, rx):
        if self.L[x] % 2 == self.NO_OPERATION or rx - lx == 1:
            return
        mx = (lx + rx)//2
        self.L[2 * x + 1] += 1
        self.T[2 * x + 1] = self.op_modify(self.T[2 * x + 1], mx - lx)
        self.L[2 * x + 2] += 1
        self.T[2 * x + 2] = self.op_modify(self.T[2 * x + 2], rx - mx)
        self.L[x] = self.NO_OPERATION

    def _update(self, l, r, x, lx, rx):
        self.propagate(x, lx, rx)
        if l >= rx or lx >= r:
            return
        if lx >= l and rx <= r:
            self.L[x] = 1
            self.T[x] = self.op_modify(self.T[x], rx - lx)
            return
        mx = (lx + rx)//2
        self._update(l, r, 2*x+1, lx, mx)
        self._update(l, r, 2*x+2, mx, rx)
        self.T[x] = self.op_sum(self.T[2*x+1], self.T[2*x+2])

    def update(self, l, r):
        return self._update(l, r, 0, 0, self.size)

    def find_k_(self, k, x, lx, rx):
        self.propagate(x, lx, rx)
        if rx - lx == 1:
            return lx
        mx = (lx + rx) // 2
        if k < self.T[2 * x + 1]:
            return self.find_k_(k, 2 * x + 1, lx, mx)
        else:
            return self.find_k_(k - self.T[2 * x + 1], 2 * x + 2, mx, rx)

    def find_k(self, k):
        return self.find_k_(k, 0, 0, self.size)

# import io, os, sys
# input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline


if __name__ == '__main__':
    n, m = [int(i) for i in input().split()]
    MOD = 10**9 + 7
    STree = SegmentTree(n)

    for i in range(m):
        t = [int(i) for i in input().split()]
        if t[0] == 1:
            STree.update(t[1], t[2])
        else:
            print(STree.find_k(t[1]))