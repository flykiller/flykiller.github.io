# we can use Segment Tree 24 and Segment Tree 31 and combine them.

class SegmentTree1:    # add arithmetic progressions
    def __init__(self, n):
        self.size = 1
        while self.size < n:
            self.size *= 2

        self.NO_OPERATION = (0, 0)  # it should be neutral with respect to op_modify
        self.ZERO = 0
        self.T = [0] * (2 * self.size - 1)
        self.L = [self.NO_OPERATION] * (2 * self.size - 1)

    def op_sum(self, a, b):
        return a + b

    def propagate(self, x, lx, rx):
        if self.L[x] == self.NO_OPERATION or rx - lx == 1:
            return
        mx = (lx + rx)//2
        a, d = self.L[x]
        a1, d1 = self.L[2 * x + 1]
        a2, d2 = self.L[2 * x + 2]
        self.L[2 * x + 1] = a + a1, d + d1
        self.L[2 * x + 2] = a + d * (mx - lx) + a2, d + d2
        self.T[2 * x + 1] += (2 * a + d*(mx - lx - 1)) * (mx - lx)//2
        self.T[2 * x + 2] += (2 * a + d*(mx + rx - 2*lx - 1)) * (rx - mx)//2
        self.L[x] = self.NO_OPERATION

    def _update(self, l, r, a, d, x, lx, rx):
        self.propagate(x, lx, rx)
        if l >= rx or lx >= r:
            return
        if lx >= l and rx <= r:
            # print("!!!!", lx, rx, l, r)
            a1, d1 = self.L[x]
            a2, d2 = a + (lx - l) * d, d
            self.L[x] = a1 + a2, d1 + d2
            self.T[x] += (2 * a2 + d2 * (rx - lx - 1)) * (rx - lx)//2
            return
        mx = (lx + rx)//2
        self._update(l, r, a, d, 2*x+1, lx, mx)
        self._update(l, r, a, d, 2*x+2, mx, rx)
        self.T[x] = self.op_sum(self.T[2*x+1], self.T[2*x+2])

    def update(self, l, r, a, d):
        return self._update(l, r, a, d, 0, 0, self.size)

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


class SegmentTree2:   # add to range, find sum on range
    def __init__(self, n, op_modify, op_sum, ZERO):
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.T = [0] * (2 * self.size - 1)   # to multiply
        self.L = [0] * (2 * self.size - 1)   # current sum
        self.op_modify = op_modify
        self.op_sum = op_sum
        self.ZERO = ZERO

    def _update(self, l, r, v, x, lx, rx):
        if l >= rx or lx >= r:
            return
        if lx >= l and rx <= r:
            self.L[x] = self.op_modify(self.L[x], v, 1)        # why 1?
            self.T[x] = self.op_modify(self.T[x], v, rx - lx)
            return
        mx = (lx + rx)//2
        self._update(l, r, v, 2*x+1, lx, mx)
        self._update(l, r, v, 2*x+2, mx, rx)
        self.T[x] = self.op_modify(self.op_sum(self.T[2*x+1], self.T[2*x+2]), self.L[x], rx - lx)

    def update(self, l, r, v):
        return self._update(l, r, v, 0, 0, self.size)

    def _query(self, l, r, x, lx, rx):
        if l >= rx or lx >= r:
            return self.ZERO
        if lx >= l and rx <= r:
            return self.T[x]
        mx = (lx + rx) // 2
        m1 = self._query(l, r, 2 * x + 1, lx, mx)
        m2 = self._query(l, r, 2 * x + 2, mx, rx)
        return self.op_modify(self.op_sum(m1, m2), self.L[x], min(rx, r) - max(lx, l))  # careful here!

    def query(self, l, r):
        return self._query(l, r, 0, 0, self.size)


if __name__ == '__main__':
    n, m = [int(i) for i in input().split()]
    STree1 = SegmentTree1(n)
    STree2 = SegmentTree2(n, lambda a, b, x: a + b*x, lambda a, b: a+b, 0)
    arr = [int(i) for i in input().split()]
    for i in range(n):
        STree1.update(i, i+1, arr[i]*(i+1), 0)  # not optimal way
        STree2.update(i, i+1, arr[i])

    print(STree1.T)
    print(STree2.T)

    for i in range(m):
        t = [int(i) for i in input().split()]
        if t[0] == 1:
            STree1.update(t[1] - 1, t[2], t[3]*t[1], t[3])
            STree2.update(t[1] - 1, t[2], t[3])
            #print(STree1.T)
            #print(STree2.T)
        else:
            m1 = STree1.query(t[1] - 1, t[2])
            m2 = STree2.query(t[1] - 1, t[2])
            print(m1 - m2*(t[1]-1))
            #print(m1, m2)