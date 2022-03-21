class SegmentTree:
    def __init__(self, n):
        self.t = [0] * (n * 4)
        self.p = [0] * (n * 4)
        self.lz = [MINF] * (n * 4)

    def push(self, x, lx, rx):
        if self.lz[x] == MINF: return
        self.t[x] = self.lz[x] * (c[rx] - c[lx])
        self.p[x] = max(0, self.t[x])
        if lx + 1 != rx:
            self.lz[2*x] = self.lz[2*x+1] = self.lz[x]
        self.lz[x] = MINF

    def upd(self, l, r, val, x, lx, rx):
        self.push(x, lx, rx)
        if lx >= r or rx <= l: return
        if lx >= l and rx <= r:
            self.lz[x] = val
            self.push(x, lx, rx)
            return
        mx = (lx + rx)//2
        self.upd(l, r, val, x*2, lx, mx)
        self.upd(l, r, val, x*2+1, mx, rx)
        self.t[x] = self.t[x*2] + self.t[x*2+1]
        self.p[x] = max(self.p[x*2], self.t[x*2] + self.p[x*2+1])

    def query(self, val, x, lx, rx):
        self.push(x, lx, rx)
        if lx + 1 == rx:
            d = self.t[x]//(c[rx] - c[lx])
            return c[lx] - 1 + val // d if self.p[x] > val else c[rx] - 1
        mx = (lx + rx)//2
        self.push(x*2, lx, mx)
        self.push(x*2 + 1, mx, rx)
        if self.p[x*2] > val:
            return self.query(val, x*2, lx, mx)
        else:
            return self.query(val - self.t[x*2], x*2+1, mx, rx)

N = int(input())
c, q = [N + 1], []

while True:
    l = input().split()
    if l[0] == "Q":
        q += [[2, int(l[1]), 0, 0]]
    elif l[0] == "I":
        q += [[1, int(l[1]), int(l[2]), int(l[3])]]
        c += [q[-1][1], q[-1][2] + 1]
    else:
        break

c = sorted(set(c))
d = {x: i for i, x in enumerate(c)}
M = len(c) - 1
MINF = -float("inf")
STree = SegmentTree(M)

for t, l, r, v in q:
    if t == 1:
        STree.upd(d[l], d[r + 1], v, 1, 0, M)
    else:
        print(STree.query(l, 1, 0, M))