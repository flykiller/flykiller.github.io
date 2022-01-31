from bisect import bisect_left, bisect
from collections import Counter
import io, os, sys
#input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline
I = lambda: [int(x) for x in input().split()]

class DSU:
    def __init__(self, N):
        self.p = list(range(N))

    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def union(self, x, y):
        xr = self.find(x)
        yr = self.find(y)
        self.p[xr] = yr

def kruskal(n, edges, XX):
    dsu, ans, sgn = DSU(n), 0, 0
    for x, y, w in edges:
        s = -1 + 2*int(XX <= w)
        if dsu.find(x) == dsu.find(y): continue
        dsu.union(x, y)
        ans += w*s
        sgn += s
    return ans, sgn


edges = []
n, m = I()
for _ in range(m):
    x, y, w = I()
    edges += [(x-1, y-1, 2*w)]

E = sorted([w for _, _, w in edges])

w, ans, out = [], [], 0

for i in range(m):
    for j in range(i, m):
        w += [(E[i]+E[j])//2]

w = sorted(set(w))
for i in range(len(w)):
    XX = w[i]
    edges = sorted(edges, key=lambda t: abs(XX - t[2]))
    ans += [kruskal(n, edges, XX)]

p, k, a, b, c = I()
Q = I()
for _ in range(k - p):
    Q += [(Q[-1] * a + b) % c]

Q2 = []
cntQ = Counter(Q)
for val in cntQ:
    if cntQ[val] % 2 == 1:
        Q2 += [val]

for x in Q2:
    t = bisect_left(w, 2*x)
    if t >= len(w): t -= 1
    out ^= (ans[t][0]//2 - x*ans[t][1])

print(out)
