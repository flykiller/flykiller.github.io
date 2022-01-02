MOD = 3
INV = {1: 1, 2: 2}

def Gauss(a):
    n, m = len(a), len(a[0]) - 1
    where = [-1] * m
    row, col = 0, 0

    while col < m and row < n:
        for i in range(row, n):
            if a[i][col]:
                a[i], a[row] = a[row], a[i]
                break

        if not a[row][col]:
            col += 1
            continue
        where[col] = row

        for i in range(n):
            if i != row:
                c = a[i][col] * INV[a[row][col] % MOD]
                for j in range(col, m + 1):
                    a[i][j] = (a[i][j] - a[row][j] * c) % MOD

        col, row = col + 1, row + 1

    ans = [0] * m
    for i in range(m):
        if where[i] != -1:
            ans[i] = (a[where[i]][m] * INV[a[where[i]][i] % MOD]) % MOD

    for i in range(n):
        sm = sum(ans[j] * a[i][j] for j in range(m))
        if (sm - a[i][m]) % MOD: return 0, [-1] * m

    if -1 in where: return 2, ans

    return 1, ans

from time import time
n = 500
from random import randint
x1 = [[randint(0, 2) for _ in range(n)] for _ in range(n-2)]
x2 = [t[:] for t in x1]
#x2 = [np.array(t) for t in x2]

t1 = time()
Gauss(x1)
t2 = time()
print(t2 - t1)