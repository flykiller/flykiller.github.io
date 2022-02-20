I = lambda: [int(i) for i in input().split()]
import io, os, sys
from math import log2
from collections import Counter


n, p = I()
arr = I()

arr_set = set(arr)
for num in sorted(arr):
    #print("NUM", num)
    x = num
    while (x % 2 == 1 or x % 4 == 0) and x > 0:
        if x % 2 == 1:
            x //= 2
        else:
            x //= 4
        if x in arr_set and x != num:
            arr_set.remove(num)
    #print("XXX", x)


arr = list(sorted(arr_set))
min_pow1 = float("inf")
min_pow2 = float("inf")

for num in arr:
    if num & (num - 1) == 0:
        x = num.bit_length() - 1
        if x % 2 == 0:
            min_pow1 = min(min_pow1, x)
        else:
            min_pow2 = min(min_pow2, x)

X = Counter()
for num in arr_set:
    X[(num - 1).bit_length()] += 1

#print("XXX", X)

start = [0, 0, 0, 0]
if 1 in arr_set:
    start[0] = 1
    start[2] = 1
    start[3] = 1

if 2 in arr_set:
    start[1] = 1
    start[3] = 1

if 3 in arr_set:
    start[2] = 1

if 4 in arr_set:
    start[3] = 1

dp = [0]*(p + 3)

#print("START", start)
#print("arr_set", arr_set)

dp[0] = start[0]
dp[1] = start[0] + start[1]
dp[2] = sum(start)

#print("MINPOW", min_pow1, min_pow2)

for i in range(p - 2):
    #print(i)
    dp[i + 3] = dp[i + 1] - dp[i] + dp[i + 2] - dp[i + 1] + dp[i + 2] + X[i + 3]
    if i % 2 == 0:
        dp[i + 3] = dp[i + 3] - int(i + 2 >= min_pow1) + int(i + 1 >= min_pow2)
    else:
        dp[i + 3] = dp[i + 3] - int(i + 2 >= min_pow2) + int(i + 1 >= min_pow1)

    dp[i + 3] %= (10**9 + 7)

#print(dp)
ans = dp[p]
if p % 2 == 0 and min_pow1 <= p:
    ans -= 1
if p % 2 == 1 and min_pow2 <= p:
    ans -= 1

print(ans % (10**9 + 7))



