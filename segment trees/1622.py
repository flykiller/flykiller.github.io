I = lambda: [int(i) for i in input().split()]

t = int(input())
for _ in range(t):
    n, m, k, q = I()
    diff = 0
    queries = [I() for _ in range(q)]
    sx = set()
    sy = set()
    for x, y in reversed(queries):
        if (x in sx and y in sy) or len(sx) == n or len(sy) == m:
            continue
        diff += 1
        sx.add(x)
        sy.add(y)
    print(pow(k, diff, 998244353))
