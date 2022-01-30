from math import gcd
import sys
input = sys.stdin.readline
I = lambda: [int(x) for x in input().split()]

class RangeQuery:
    def __init__(self, data, func):
        self.func = func
        self._data = _data = [data]
        i, n = 1, len(_data[0])
        while 2 * i <= n:
            prev = _data[-1]
            _data.append([func(prev[j], prev[j + i]) for j in range(n - 2 * i + 1)])
            i <<= 1

    def query(self, L, R):
        depth = (R - L).bit_length() - 1
        return self.func(self._data[depth][L], self._data[depth][R - (1 << depth)])

n = int(input())
arr = I()
STable = RangeQuery(arr, gcd)
ints = {}

for i in range(n):
    beg, end = i, n
    while beg + 1 < end:
        mid = (beg + end)//2
        if STable.query(i, mid + 1) >= mid - i + 1:
            beg = mid
        else:
            end = mid

    if STable.query(i, end) == end - i:
        ints[end - 1] = i

dp = [0] * (n + 1)
for i in range(1, n + 1):
    dp[i] = dp[i-1] if i-1 not in ints else dp[ints[i-1]] + 1

print(" ".join(str(x) for x in dp[1:]))