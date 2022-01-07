from itertools import combinations
from collections import defaultdict
import io, os, sys
# input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline

def F1(A, B, C, D):
    E = (A & D) ^ (B & C)
    return A ^ C ^ E ^ (B & D), B ^ D ^ E ^ (A & C)

def F2(A, B, C, D):
    E = (A & C) ^ (B & D)
    return A ^ D ^ E ^ (B & C), B ^ C ^ E ^ (A & D)

def Gauss(a, b, n, m):
    if n == 0: return 2, [0] * m
    where = [-1] * m
    row, col = 0, 0

    while col < m and row < n:
        t1, t2 = divmod(col, l)
        for i in range(row, n):
            if a[i][t1] >> t2 & 1 or b[i][t1] >> t2 & 1:
                a[i], a[row] = a[row], a[i]
                b[i], b[row] = b[row], b[i]
                break

        if not a[row][t1] >> t2 & 1 and not b[row][t1] >> t2 & 1:
            col += 1
            continue
        where[col] = row

        for i in range(n):
            if i == row: continue
            x1, x2 = a[i][t1] >> t2 & 1, b[i][t1] >> t2 & 1
            y1, y2 = a[row][t1] >> t2 & 1, b[row][t1] >> t2 & 1
            cc = ((x1 + 2*x2) * (y1 + 2*y2)) % 3
            if cc == 0: continue
            F = F1 if cc == 2 else F2
            for k in range(t1, U): a[i][k], b[i][k] = F(a[i][k], b[i][k], a[row][k], b[row][k])

        col, row = col + 1, row + 1

    ans = [0] * m
    t1, t2 = divmod(m, l)
    for i in range(m):
        W = where[i]
        if W != -1:
            t3, t4 = divmod(i, l)
            x1, x2 = a[W][t1] >> t2 & 1, b[W][t1] >> t2 & 1
            y1, y2 = a[W][t3] >> t4 & 1, b[W][t3] >> t4 & 1
            ans[i] = ((x1 + 2*x2) * (y1 + 2*y2)) % 3

    for i in range(n):
        sm = 0
        for j in range(m):
            t3, t4 = divmod(j, l)
            sm += ((a[i][t3] >> t4 & 1) + 2 * (b[i][t3] >> t4 & 1)) * ans[j]

        if sm % 3 != (a[i][t1] >> t2 & 1) + 2 * (b[i][t1] >> t2 & 1): return 0, [-1] * m

    if -1 in where: return 2, ans
    return 1, ans


T = int(input())
for _ in range(T):
    n, m = [int(i) for i in input().split()]
    l, U = 63, m//63 + 1

    G = defaultdict(list)
    edges_back = {}
    colors = [0] * m
    for k in range(m):
        a, b, c = [int(i) for i in input().split()]
        G[a] += [(b, c)]
        G[b] += [(a, c)]
        edges_back[(a, b)] = (k, c)
        edges_back[(b, a)] = (k, c)
        colors[k] = c

    ans = set()
    for n1 in range(1, n + 1):
        neibs = G[n1]
        for (n2, c12), (n3, c13) in combinations(neibs, 2):
            if (n2, n3) in edges_back:
                row = [[0] * U, [0] * U]
                k12, _ = edges_back[(n1, n2)]
                k13, _ = edges_back[(n1, n3)]
                k23, c23 = edges_back[(n2, n3)]
                last = 0
                for k, c in (k12, c12), (k13, c13), (k23, c23):
                    if c != -1:
                        last -= c
                    else:
                        flip_bit(row[0], k)
                last %= 3
                if last == 1:
                    flip_bit(row[0], m)
                elif last == 2:
                    flip_bit(row[1], m)

                ans.add(tuple(tuple(x) for x in row))

    mat1, mat2 = [], []
    for x, y in ans:
        mat1 += [list(x)]
        mat2 += [list(y)]

    ans = Gauss(mat1, mat2, len(mat1), m)

    if ans[0] == 0:
        out = [-1]
    else:
        out = []
        for i in range(m):
            if colors[i] != -1:
                out += [colors[i]]
            elif ans[1][i] == 0:
                out += [3]
            else:
                out += [ans[1][i]]

    print(" ".join(str(x) for x in out))
