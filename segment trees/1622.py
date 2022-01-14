I = lambda: [float(x) for x in input().split()]
n, m = [int(i) for i in input().split()]
V = [I() for _ in range(n)]
cmp = lambda x: (x >= 0) - (x <= 0)

for _ in range(m):
    x0, y0, x1, y1 = I()
    p0, p1 = x1 - x0, y1 - y0
    V3 = [((x - x0) * p0 + (y - y0) * p1, (y - y0) * p0 - (x - x0) * p1) for x, y in V]
    res = []

    for (v1x, v1y), (v2x, v2y) in zip(V3, V3[1:] + V3[:1]):
        if cmp(v1y) != cmp(v2y):
            res.append(((v2x * v1y - v1x * v2y) / (v1y - v2y), cmp(v2y) - cmp(v1y)))

    res.sort()

    t, w = 0, 0.
    for i in range(1, len(res)):
        t += res[i - 1][1]
        if t: w += res[i][0] - res[i-1][0]

    print(w / (p0 * p0 + p1 * p1) ** 0.5)