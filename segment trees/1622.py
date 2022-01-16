from collections import defaultdict
I = lambda: [int(x) for x in input().split()]
import io, os, sys
#input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline

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

class Counter:
    def __init__(self, c):
        self.ans = c
        self.c_t = defaultdict(lambda: 0)
        self.mx = self.c_t[c] = 1
        self.t_c = defaultdict(set)
        self.t_c[1] = {c}

    def merge(self, other):
        for c, t in other.c_t.items():
            self.add(c, t)

    def add(self, c, t):
        old_t = self.c_t[c]
        self.c_t[c] = new_t = old_t + t
        self.t_c[old_t].discard(c)
        self.t_c[new_t].add(c)
        if new_t == self.mx:
            self.ans += c
        elif new_t > self.mx:
            self.mx = new_t
            self.ans = c

    def __len__(self):
        return len(self.c_t)

    def __repr__(self):
        return str(self.ans)

@bootstrap
def dfs(par, node):
    c = color[node]
    ans_n = Counter(c)

    for child in G[node]:
        if child == par: continue
        ans_c = yield dfs(node, child)
        if len(ans_n) < len(ans_c):
            ans_n, ans_c = ans_c, ans_n
        ans_n.merge(ans_c)
    out[node] = ans_n.ans
    yield ans_n

n = int(input())
color = I()
G = defaultdict(list)
out = [0]*n
for _ in range(n-1):
    a, b = I()
    G[a-1] += [b-1]
    G[b-1] += [a-1]

dfs(-1, 0)
sys.stdout.write(" ".join(map(str, out)) + "\n")

