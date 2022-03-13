# this segment tree will support two operations:
# 1. set segment [r, l) equal to v
# 2. For segment [r, l) find number of black parts and their length
# We will keep tuple with 4 elements for T:
# number of black parts, their total length, color of left and right ends
# For L we will keep one value 0 or 1: the lazy update for color


class SegmentTree:
    def __init__(self, n):
        self.size = 1
        while self.size < n:
            self.size *= 2

        self.NO_OPERATION = -float("inf")  # it should be neutral with respect to op_modify
        self.ZERO = (0, 0, 0, 0)
        self.T = [self.ZERO] * (2 * self.size - 1)
        self.L = [self.NO_OPERATION] * (2 * self.size - 1)

    def op_sum(self, a, b):
        return a[0] + b[0] - int(a[3] == 1 and b[2] == 1), a[1] + b[1], a[2], b[3]

    def propagate(self, x, lx, rx):
        if self.L[x] == self.NO_OPERATION or rx - lx == 1:
            return
        mx = (lx + rx)//2
        if self.L[x] == 0:
            self.L[2 * x + 1] = 0
            self.L[2 * x + 2] = 0
            self.T[2 * x + 1] = (0, 0, 0, 0)
            self.T[2 * x + 2] = (0, 0, 0, 0)
        else:
            self.L[2 * x + 1] = 1
            self.L[2 * x + 2] = 1
            self.T[2 * x + 1] = (1, mx - lx, 1, 1)
            self.T[2 * x + 2] = (1, rx - mx, 1, 1)
        self.L[x] = self.NO_OPERATION

    def _update(self, l, r, color, x, lx, rx):
        self.propagate(x, lx, rx)
        if l >= rx or lx >= r:
            return
        if lx >= l and rx <= r:
            if color == 0:
                self.T[x] = (0, 0, 0, 0)
                self.L[x] = 0
            else:
                self.T[x] = (1, rx - lx, 1, 1)
                self.L[x] = 1
            return
        mx = (lx + rx)//2
        self._update(l, r, color, 2*x+1, lx, mx)
        self._update(l, r, color, 2*x+2, mx, rx)
        self.T[x] = self.op_sum(self.T[2*x+1], self.T[2*x+2])

    def update(self, l, r, color):
        return self._update(l, r, color, 0, 0, self.size)

# import sys
# input = sys.stdin.readline


if __name__ == '__main__':
    n = 500001
    m = int(input())
    STree = SegmentTree(2*n)

    for i in range(m):
        t = [i for i in input().split()]
        l, r = int(t[1]) + n, int(t[1]) + int(t[2]) + n
        if t[0] == "W":
            STree.update(l, r, 0)
        else:
            STree.update(l, r, 1)
        x = STree.T[0]
        print(str(x[0]) + " " + str(x[1]))