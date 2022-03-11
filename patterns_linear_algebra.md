---
layout: page
title: Patterns Linear Algebra
permalink: /patterns/linear algebra
---

Here is a collection of different linear algebra algorithms.


#### Fast matrix modulo expontiation
Given $A$ $T\times T$ size square matrix, we need to evaluate $A^n$ modulo `MOD`. It can be done in $O(T^3\log n)$ time, using doubling trick. It is useful for some types of dynamic programming problems. If we use classical `MOD = 10^9 + 7`, then to avoid overflow we can use this only in case when $T\leqslant 8$. Depending on problem specific it can work for $T > 8$, but we can not be sure.

```python
def power(M, n, MOD):
    result = np.eye(len(M), dtype = np.int64)
    while n > 0:
        if n%2: result = np.dot(M, result) % MOD
        M = np.dot(M, M) % MOD
        n //= 2
    return result
```

If we want to make it work for $T > 8$ we have to used slower version with multiplication by hands:

```python
def mult(X, Y, MOD):
    return [[sum(a*b for a,b in zip(x, y))%MOD for y in zip(*Y)] for x in X]
        
def power(M, n, MOD):
    result = [[0] * len(M) for _ in range(len(M))]
    for i in range(len(M)): result[i][i] = 1
    while n > 0:
        if n%2: result = mult(M, result, MOD)
        M = mult(M, M, MOD)
        n //= 2
    return result
```

#### Matrix operations
Here is a bunch of matrix operation, which can be useful if numpy is not allowed.

```python
from copy import deepcopy

transpose = lambda mat: [list(col) for col in zip(*mat)]

minor = lambda mat, i, j: [row[:j] + row[j + 1:] for row in (mat[:i] + mat[i + 1:])]

mat_add = lambda *mat: [[sum(elements) for elements in zip(*row)] for row in zip(*mat)]

mat_sub = lambda A, B: [[i - j for i, j in zip(*row)] for row in zip(A, B)]

mat_mul = lambda A, B: [[sum(i * j for i, j in zip(row, col)) for col in zip(*B)] for row in A]

vec_mul = lambda mat, vec: [sum(a * b for a, b in zip(row, vec)) for row in mat]

def eye(m):
    """returns an indentity matrix of order m"""
    identity = [[0] * m for _ in range(m)]
    for i, row in enumerate(identity):
        row[i] = 1
    return identity
```


#### Gauss elimination modulo p
Imagine that we have linear system of equation modulo p. Then we can use Gaussian elimination to solve this system.
1. If we have only one solution it will return 1, solution
2. If we have infinity solutions, it will return 2, some solution.
3. If we have not solutions, it will return 0, [-1]*n

```python
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
                for j in range(col, m+1):
                    a[i][j] -= a[row][j] * c

        col, row = col + 1, row + 1

    ans = [0] * m
    for i in range(m):
        if where[i] != -1:
            ans[i] = (a[where[i]][m] * INV[a[where[i]][i] % MOD]) % MOD

    for i in range(n):
        sm = sum(ans[j] * a[i][j] for j in range(m))
        if (sm - a[i][m]) % MOD: return 0, [-1]*m

    if -1 in where: return 2, ans
            
    return 1, ans
```

#### Gauss elimination modulo 2
We can make previous code faster 63 times if we use bitmasks (on python 64 bit compilator).

#### Gauss elimination modulo 3
Moreover, we can make fast modulo 3 gauss elimination if we use bunch of bit tricks. The idea is for each number keep two bitmasks:
If we have `(0, 0)` then we have `0`, if we have `(1, 0)`, then we have `1` and if we have `(1, 1)`, then we have `2`. Notice that we will never have `(0, 1)`.
1. Function `F1` used to add two numbers with representation `(A, B)` and `(C, D)`.
2. Function `F2` used to subtract two numbers with representation `(A, B)` and `(C, D)`.
3. Input parameters of `Gauss` functions are two bitmasks `a` and `b` (represented as list of 63 bit numbers) which correspond to extended matrix, that is if we have `Ux = v` system, it is matrix `U` with vector `v` concatenated.

In practice we have gain approximately equal to `63/6` times, because this number of opertions we need to do in our bottleneck, when we update rows.

```python
l, U = 63, m//63 + 1

def F1(A, B, C, D):
    AD = A ^ D
    return (AD ^ B) | (A ^ C), AD & (B ^ C)

def F2(A, B, C, D):
    AC = A ^ C
    return AC | (B ^ D), (AC ^ D) & (B ^ C)

def Gauss(a, b, n, m):
    if n == 0: return 2, [0] * m
    where = [-1] * m
    row, col = 0, 0
    S = 0

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
            cc = ((x1 + x2) * (y1 + y2)) % 3
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
            ans[i] = ((x1 + x2) * (y1 + y2)) % 3

    for i in range(n):
        sm = 0
        for j in range(m):
            t3, t4 = divmod(j, l)
            sm += ((a[i][t3] >> t4 & 1) + (b[i][t3] >> t4 & 1)) * ans[j]

        if (sm - (a[i][t1] >> t2 & 1) - (b[i][t1] >> t2 & 1)) % 3 != 0: return 0, [-1] * m

    if -1 in where: return 2, ans
    return 1, ans
```