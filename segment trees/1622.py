M, N, res = 998244353, 720720, 0
I = lambda: [int(x) for x in input().split()]
p = [0] * N

n, a, x, y, k, U = I()
for i in range(1, n + 1):
    p[a % N] += 1
    res += a // N * N
    a = (a * x + y) % U

res = (res * pow(n, k - 1, M) * k) % M
for i in range(1, k + 1):
    tot = sum(p[j] * j for j in range(N)) % M
    for j in range(N):
        tmp = p[j]
        p[j] *= (n - 1)
        p[j] %= M
        p[j - j % i] += tmp
    res += (tot * pow(n, k - i)) % M

print(res % M)