I = lambda: [int(i) for i in input().split()]
import io, os, sys
#input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline

class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.rnk = [0] * n
        self.lft = list(range(n))
        self.rgh = list(range(n))
        self.lst = [n - 1] * n

    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def union(self, x, y):
        x, y = self.find(x), self.find(y)
        if x == y: return False
        if self.rnk[x] > self.rnk[y]:
            x, y = y, x
        self.p[x] = self.p[y]
        if self.rnk[x] == self.rnk[y]:
            self.rnk[y] += 1
        self.lft[y] = min(self.lft[x], self.lft[y])
        self.rgh[y] = max(self.rgh[x], self.rgh[y])
        self.lst[y] = min(self.lst[x], self.lst[y])
        return True

    def find_lft(self, x):
        return self.lft[dsu.find(x)]

    def find_rgh(self, x):
        return self.rgh[dsu.find(x)]

    def find_lst(self, x):
        return self.lst[dsu.find(x)]

n, q = I()
dsu, ans = DSU(n + 2), []
for _ in range(q):
    args = I()
    if args[0] == 0:
        l, r, x = args[1:]
        idx_l = dsu.find(l - 1)
        idx_r = dsu.find(r)
        if x:
            dsu.lst[idx_l] = min(dsu.lst[idx_l], r)
        else:
            beg, end = dsu.rgh[idx_l], dsu.lft[idx_r]
            while beg < end:
                dsu.union(beg, beg + 1)
                beg = dsu.find_rgh(beg)
    else:
        j = args[1]
        if dsu.find(j - 1) == dsu.find(j):
            ans += ["NO"]
        elif dsu.find_lft(dsu.find_lst(j - 1)) == j:
            ans += ["YES"]
        else:
            ans += ["N/A"]

print("\n".join(ans))