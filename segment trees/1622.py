from collections import defaultdict
#import io, os, sys

#input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline

n, l, k = [int(i) for i in input().split()]
arr_d = [int(i) for i in input().split()] + [l]
arr_a = [int(i) for i in input().split()] + [0]
diff = [x - y for x, y in zip(arr_d[1:], arr_d)]

dp = {(k, arr_a[0]): 0}

for i in range(1, n + 1):
    dp2 = defaultdict(lambda: float("inf"))
    for (k1, sp), val in dp.items():
        t, s = arr_a[i - 1], diff[i - 1]
        dp2[k1, t] = min(dp2[k1, t], val + t * s)
        if k1 >= 1 and t > sp: dp2[k1 - 1, sp] = min(dp2[k1 - 1, sp], val + sp * s)
    dp = dp2

print(min(dp.values()))