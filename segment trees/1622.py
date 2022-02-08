import io, os, sys
#input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline
I = lambda: [int(x) for x in input().split()]

def update(i, d, cnt):
    cnt -= (unfib[i] != 0)
    unfib[i] = (unfib[i] + d) % MOD
    cnt += (unfib[i] != 0)
    return cnt

n, q, MOD = I()
a = I()
b = I()
diff = [0, 0] + [(y - x) % MOD for x, y in zip(a, b)]
fib = [1] * n
for i in range(2, n):
    fib[i] = (fib[i - 1] + fib[i - 2]) % MOD

unfib = [(diff[i+2] - diff[i + 1] - diff[i]) % MOD for i in range(n)]

cnt = sum(x != 0 for x in unfib)
result = []
for _ in range(q):
    c, l, r = input().split()
    l, r = int(l) - 1, int(r) - 1
    sign = 1 if c == 'A' else -1
    cnt = update(l, -sign, cnt)
    if r + 1 < n: cnt = update(r + 1, sign * fib[r - l + 1], cnt)
    if r + 2 < n: cnt = update(r + 2, sign * fib[r - l], cnt)
    result += ["YES" if cnt == 0 else "NO"]

sys.stdout.write("\n".join(result))