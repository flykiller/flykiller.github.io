from collections import defaultdict, Counter
I = lambda: [int(x) for x in input().split()]

################################################
from types import GeneratorType
def bootstrap(f, stack=[]):
    def wrappedfunc(*args, **kwargs):
        if stack:
            return f(*args, **kwargs)
        else:
            to = f(*args, **kwargs)
            while True:
                if type(to) is GeneratorType:
                    stack.append(to)
                    to = next(to)
                else:
                    stack.pop()
                    if not stack:
                        break
                    to = stack[-1].send(to)
            return to
    return wrappedfunc
################################################


@bootstrap
def dfs1(u, p):
    cnt[u] = c[u]
    for v in G[u]:
        if v == p: continue
        yield dfs1(v, u)
        cnt[u] += cnt[v]
        if ans[v] and cnt[v] >= 2: ans[u] = 1
    yield


@bootstrap
def dfs2(u, p):
    for v in G[u]:
        if v == p: continue
        if ans[u] and tot - cnt[v] >= 2: ans[v] = 1
        yield dfs2(v, u)
    yield

n = int(input())
c = I()
cnt, ans = [0]*n, [0]*n
G = defaultdict(list)
tot = sum(c)
for i in range(n-1):
    u, v = I()
    G[u-1] += [v-1]
    G[v-1] += [u-1]

for i in range(n):
    if not c[i]: continue
    ans[i] = 1
    for v in G[i]: ans[v] = 1

dfs1(0, -1)
dfs2(0, -1)

print(" ".join(map(str, ans)) + "\n")