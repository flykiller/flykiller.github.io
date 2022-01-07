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

def get_bit(a, i):
    return a[i // l] >> (i % l) & 1

def flip_bit(a, i):
    a[i // l] ^= (1 << (i % l))

def Gauss(a, b, n, m):
    if n == 0: return 2, [0] * m
    where = [-1] * m
    row, col = 0, 0

    while col < m and row < n:
        for i in range(row, n):
            if get_bit(a[i], col) or get_bit(b[i], col):
                a[i], a[row] = a[row], a[i]
                b[i], b[row] = b[row], b[i]
                break

        if not get_bit(a[row], col) and not get_bit(b[row], col):
            col += 1
            continue
        where[col] = row

        for i in range(n):
            if i != row:
                x1, x2 = get_bit(a[i], col), get_bit(b[i], col)
                y1, y2 = get_bit(a[row], col), get_bit(b[row], col)
                cc = ((x1 + 2*x2) * (y1 + 2*y2)) % 3
                if cc == 0: continue
                F = F1 if cc == 2 else F2
                for k in range(U): a[i][k], b[i][k] = F(a[i][k], b[i][k], a[row][k], b[row][k])

        col, row = col + 1, row + 1

    ans = [0] * m
    for i in range(m):
        if where[i] != -1:
            x1, x2 = get_bit(a[where[i]], m), get_bit(b[where[i]], m)
            y1, y2 = get_bit(a[where[i]], i), get_bit(b[where[i]], i)
            ans[i] = ((x1 + 2*x2) * (y1 + 2*y2)) % 3

    for i in range(n):
        sm = sum((get_bit(a[i], j) + 2 * get_bit(b[i], j)) * ans[j] for j in range(m))
        if sm % 3 != get_bit(a[i], m) + 2 * get_bit(b[i], m): return 0, [-1] * m

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
