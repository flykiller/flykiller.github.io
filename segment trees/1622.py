from bisect import bisect_left, bisect
import io, os, sys
from collections import Counter
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
        s =  -1 + 2*int(XX <= w)
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
ans = [(-1, -1)] * len(w)

#for i in range(len(w)):
#    edges = sorted(edges, key=lambda t: abs(w[i] - t[2]))
#    ans[i] = kruskal(n, edges, w[i])

p, k, a, b, c = I()
Q = I()
for _ in range(k - p):
    Q += [(Q[-1] * a + b) % c]

cc = Counter(Q)
Q = [ee for ee in cc if (cc[ee] % 2 == 1)]
Q.sort()

t = 0
for x in Q:
    while t < len(w) - 1 and w[t] < 2*x: t += 1
    if ans[t] == (-1, -1):
        edges = sorted(edges, key=lambda q: abs(w[t] - q[2]))
        ans[t] = kruskal(n, edges, w[t])
    out ^= (ans[t][0]//2 - x*ans[t][1])

print(out)