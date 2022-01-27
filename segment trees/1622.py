I = lambda: [int(i) for i in input().split()]
n = int(input())
arr = I()
last = {x: i for i, x in enumerate(arr)}

lastest, covered, ans = 0, 0, 0
for i, x in enumerate(arr):
    lastest = max(lastest, last[x])
    if covered > i:
        ans += 1
    else:
        covered = lastest

print(ans)