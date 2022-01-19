from collections import defaultdict

def perm_loops(x, n): # from permutation create loops, permutation eg [1, 0, 4, 2, 3]
    V, ans = set(), []
    for i in range(n):
        if i in V: continue
        q = i
        ans += [[q]]
        V.add(i)
        while x[q] != i:
            ans[-1] += [x[q]]
            q = x[q]
            V.add(q)
    return ans

def loops_perm(loops, n):  # from loops create permutation
    ans = [0] * n
    for loop in loops:
        for x, y in zip(loop, loop[1:] + loop[:1]):
            ans[x] = y
    return ans

n = int(input())
arr = [int(i) - 1 for i in input().split()]
d_loops = defaultdict(list)

loops = perm_loops(arr, n)
for loop in loops:
    d_loops[len(loop)] += [tuple(loop)]

def solve(d_loops):
    ans = []
    for d in d_loops:
        if d % 2 == 1:
            for loop in d_loops[d]:
                tmp = [0]*d
                tmp[::2] = loop[:d//2+1]
                tmp[1::2] = loop[d//2+1:]
                ans += [tmp]
        else:
            if len(d_loops[d]) % 2 == 1:
                return []
            else:
                for i in range(len(d_loops[d])//2):
                    tmp = [0]*(2*d)
                    tmp[::2] = d_loops[d][2*i]
                    tmp[1::2] = d_loops[d][2*i+1]
                    ans += [tmp]
    return ans

ans = solve(d_loops)
if ans == []:
    print(-1)
else:
    out = loops_perm(ans, n)
    print(" ".join(str(i+1) for i in out))