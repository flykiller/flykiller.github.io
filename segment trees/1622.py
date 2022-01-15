I = lambda: [int(x) for x in input().split()]

T, INF = int(input()), float("inf")
for _ in range(T):
    n, m, k = I()
    x = I()

    dic = [{} for i in range(n+1)]
    a_bcdh = [[] for i in range(n+1)]

    for i in range(k):
        a, b, c, d, h = I()
        a_bcdh[a] += [(b, c, d, h)]
        dic[a][b] = dic[c][d] = INF

    dic[1][1] = 0
    dic[n][m] = INF

    for a in range(1, n + 1):
        level = sorted(dic[a])
        for u, v in zip(level, level[1:]):
            dic[a][v] = min(dic[a][v], dic[a][u] + abs(u - v) * x[a - 1])

        level = level[::-1]
        for u, v in zip(level, level[1:]):
            dic[a][v] = min(dic[a][v], dic[a][u] + abs(u - v) * x[a - 1])

        for b, c, d, h in a_bcdh[a]:
            dic[c][d] = min(dic[c][d], dic[a][b] - h)

    print("NO ESCAPE" if dic[n][m] == INF else dic[n][m])