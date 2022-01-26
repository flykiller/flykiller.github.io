from collections import defaultdict
from itertools import combinations, product
import io, os, sys
input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline
sys.setrecursionlimit(3000)

I = lambda: [int(i) for i in input().split()]
n = int(input())
A = [I() for _ in range(n)]


def check(arr, LIM):
    if len(arr) == 1:
        return (True, 0)

    d = defaultdict(list)
    pivot = arr[0]
    for x in arr[1:]:
        d[A[pivot][x]] += [x]

    vals = sorted(d.keys())
    for x, y in combinations(vals, 2):
        for i1, i2 in product(d[x], d[y]):
            if A[i1][i2] != y: return (False, 0)

    max_val = vals[-1]
    for x in vals:
        res, vl = check(d[x], x)
        if not res: return (False, 0)
        max_val = max(max_val, vl)

    return (False, 0) if max_val > LIM else (True, max_val)


def solve():
    for i in range(n):
        for j in range(i + 1, n):
            if A[i][j] != A[j][i]: return False
        if A[i][i] != 0: return False
    return check(list(range(n)), float("inf"))[0]


print("MAGIC" if solve() else "NOT MAGIC")