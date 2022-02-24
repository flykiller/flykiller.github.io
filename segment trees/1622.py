class SegmentTree:
    def __init__(self, n):
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.T = [0] * (2 * self.size - 1)   # to multiply
        self.L = [0] * (2 * self.size - 1)   # current sum
        self.ZERO = 0  # neutral element, for min it is +inf
        self.NO_OPERATION = -float("inf")  # this is for our propagate to understand that we do not need it

    def op_modify(self, a, b, len_):
        if b == self.NO_OPERATION:
            return a
        return b * len_

    def op_sum(self, a, b):
        return max(a, b)

    def propagate(self, x, lx, rx):
        if self.L[x] == self.NO_OPERATION or rx - lx == 1:
            return
        mx = (lx + rx)//2
        self.L[2 * x + 1] = self.op_modify(self.L[2 * x + 1], self.L[x], 1)
        self.T[2 * x + 1] = self.op_modify(self.T[2 * x + 1], self.L[x], mx - lx)  # in fact we do not use len
        self.L[2 * x + 2] = self.op_modify(self.L[2 * x + 2], self.L[x], 1)
        self.T[2 * x + 2] = self.op_modify(self.T[2 * x + 2], self.L[x], rx - mx)
        self.L[x] = self.NO_OPERATION

    def _update(self, l, r, v, x, lx, rx):
        self.propagate(x, lx, rx)
        if l >= rx or lx >= r:
            return
        if lx >= l and rx <= r:
            self.L[x] = self.op_modify(self.L[x], v, 1)        # why 1?
            self.T[x] = self.op_modify(self.T[x], v, rx - lx)
            return
        mx = (lx + rx)//2
        self._update(l, r, v, 2*x+1, lx, mx)
        self._update(l, r, v, 2*x+2, mx, rx)
        self.T[x] = self.op_sum(self.T[2*x+1], self.T[2*x+2])

    def update(self, l, r, v):
        return self._update(l, r, v, 0, 0, self.size)

    def _query(self, l, r, x, lx, rx):
        self.propagate(x, lx, rx)
        if l >= rx or lx >= r:
            return self.ZERO
        if lx >= l and rx <= r:
            return self.T[x]
        mx = (lx + rx) // 2
        m1 = self._query(l, r, 2 * x + 1, lx, mx)
        m2 = self._query(l, r, 2 * x + 2, mx, rx)
        return self.op_sum(m1, m2)

    def query(self, l, r):
        return self._query(l, r, 0, 0, self.size)

    def first_above_(self, v, l, x, lx, rx):
        self.propagate(x, lx, rx)
        if self.T[x] < v or rx <= l:
            return -1
        if rx - lx == 1:
            return lx
        mx = (lx + rx) // 2
        res = self.first_above_(v, l, 2 * x + 1, lx, mx)
        if res == -1:
            res = self.first_above_(v, l, 2 * x + 2, mx, rx)
        return res

    def first_above(self, v, l):
        return self.first_above_(v, l, 0, 0, self.size)

I = lambda: [int(i) for i in input().split()]

n, q = I()
STree = SegmentTree(n)
STree.update(0, n, 1)


ill = set()

for _ in range(q):
    arr = I()
    if arr[0] == 0 and arr[3] == 0:
        STree.update(arr[1] - 1, arr[2], 0)
    elif arr[0] == 0 and arr[3] == 1:
        sm = STree.query(arr[1] - 1, arr[2])
        l, r = arr[1] - 1, arr[2] + 1
        while l + 1 < r:
            m = (l + r)//2
            if STree.query(l, r) == 1:
                r = m
            else:
                l = m
        ill.add(l + 1)
    else:
        tt = arr[1] - 1
        if tt in ill:
            print("YES")
        elif STree.query(tt, tt + 1) == 0:
            print("NO")
        else:
            print("N/A")

    #print("ILL", ill)

