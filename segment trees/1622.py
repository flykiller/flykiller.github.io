from collections import Counter

def calc(a, d, m):
    dp1 = [0]*m
    dp2 = [1] + [0]*(m-1)
    for i in range(len(a)):
        dp11, dp21 = [0] * m, [0] * m
        ai = int(a[i])
        start = 1 if i == 0 else 0
        c1 = [d] if i % 2 == 1 else set(range(start, 10)) - set([d])
        c2 = set(range(start, ai)) - set([d]) if i % 2 == 0 else [d] if d < ai else []
        c3 = set([ai]) - set([d]) if i % 2 == 0 else [d] if ai == d else []
        for x in range(m):
            for c in c1: dp11[(x*10 + c) % m] += dp1[x]
            for c in c2: dp11[(x*10 + c) % m] += dp2[x]
            for c in c3: dp21[(x*10 + c) % m] += dp2[x]

        dp1, dp2 = [i%N for i in dp11], [i%N for i in dp21]
    return dp1[0] + dp2[0]

m, d = [int(i) for i in input().split()]
N = 10**9 + 7
a = input().rstrip()
b = input().rstrip()

t1 = calc(a, d, m)
t2 = calc(b, d, m)
addon = a[1::2] == str(d)*len(a[1::2]) and a[::2].count(str(d)) == 0 and int(a) % m == 0

print((t2 - t1 + addon) % N)