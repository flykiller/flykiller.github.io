from bisect import bisect_left
from collections import defaultdict
I = lambda: [int(x) for x in input().split()]

class DSU:
    def __init__(self, N):
        self.p = list(range(N))

    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def union(self, x, y):
        self.p[self.find(x)] = self.find(y)


edges = []
n, m = I()
for _ in range(m):
    x, y, w = I()
    edges += [(x - 1, y - 1, w)]

p, k, a, b, c = I()
Q = I()
for _ in range(k - p):
    Q += [(Q[-1] * a + b) % c]

def kruskal(x):
    dsu, ans, W, sgn = DSU(n), [], 0, 0
    E = sorted(edges, key=lambda q: abs(x - q[2]))
    for u, v, w in E:
        if dsu.find(u) == dsu.find(v): continue
        s = -1 + 2 * int(x <= w)
        dsu.union(u, v)
        ans += [w]
        W += w * s
        sgn += s
    return sorted(ans), W, sgn

points = defaultdict(tuple)
at, maxval = 0, 10**8

while at <= maxval:
    cur_weights, wei, sgn = kruskal(at)
    lo, hi = at, maxval
    while lo < hi:
        mid = (lo + hi + 1) // 2
        cur_weights2, wei2, sgn2 = kruskal(mid)
        if cur_weights2 == cur_weights:
            lo = mid
        else:
            hi = mid - 1

    points[lo] = kruskal(lo)
    at = lo + 1

for _, _, w in edges:
    points[w] = kruskal(w)

w, out = sorted(points), 0

for x in Q:
    idx = bisect_left(w, x)
    if idx >= len(w): idx -= 1
    out ^= (points[w[idx]][1] - x*points[w[idx]][2])

print(out)