import sys
input = sys.stdin.readline

M = 998244353
Q = lambda x: pow(2, x, M) - 1
get = lambda A, i: [[y for y in A if y >> i & 1 == b] for b in (0, 1)]

def f2(A, B, i):
    if not A or not B or i == -1: return Q(len(A) + len(B))
    A0, A1 = get(A, i)
    B0, B1 = get(B, i)
    if x >> i & 1:
        return ((f2(A0, B1, i - 1) + 1) * (f2(A1, B0, i - 1) + 1) - 1) % M
    else:
        return (f2(A0, B0, i - 1) + f2(A1, B1, i - 1) + Q(len(A0)) * Q(len(A1)) + Q(len(B0)) * Q(len(B1))) % M

        return f(x,y,i-1)+f(w,z,i-1)+q(x)*q(y)+q(w)*q(z)
        return (f(x, y, i - 1) + q(x) + q(y) + 1) * (f(w, z, i - 1) + q(w) + q(z) + 1) - q(a) - q(b) - 1

def f1(A, i):
    if not A: return Q(len(A))
    A0, A1 = get(A, i)
    return f2(A0, A1, i - 1) if x >> i & 1 else (f1(A0, i - 1) + f1(A1, i - 1)) % M

n, x = [int(i) for i in input().split()]
arr = [int(i) for i in input().split()]
print(f1(arr, 29))