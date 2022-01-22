I = lambda: [int(i) for i in input().split()]

N, LOGN = 100100, 20
INF = float("inf")

n, m = I()
a = I()
a = []
for i in range(m):
    a, b = I()
    q += [((a, b), i)]


def getXOR(a):
    return [a, 1, a+1, 0][a%4]

class Node:
    def __init__(self, nt=[-1, -1], maxv=-INF):
        self.nt = nt
        self.maxv = maxv

szt = [0, 0]
root = [0, 0]
t0, t1 = [Node()] * (N * LOGN)

def lift(ti, v):    #ti: trie number, v: node
    tmp = t0 if ti == 0 else t1
    tmp[v].maxv = -INF
    for nv in tmp[nt]:
        if nv != -1:
            tmp[v].maxv = max(tmp[v].maxv, tmp[nv].maxv)

def calc(ti, x, minv):
    v = root[ti]
    tmp = t0 if ti == 0 else t1
    if minv > t[v].maxv: return 0
    ans = 0
    for i in range(LOGN):
        d = (x >> i) & 1
        for jj in range(2):
            j = jj ^ d
            vv = tmp[v].nt[j]
            if vv != -1 and minv <= tmp[vv].maxv:
                v = tmp[v].nt[j]
                if jj: ans |= 1 << i
                break
    return ans

def add(ti, x, curv):
    v = root[ti]
    tmp = t0 if ti == 0 else t1
    szvs = 0
    vs = [0]*LOGN
    for i in range(LOGN):
        vs[szvs+1] = v
        szvs += 1
        d = (x >> i) & 1
        nt = t[v].nt[d]
        if nt == -1: nt = newNode(ti)
        v = nt

    t[v].maxv = max(t[v].maxv, curv)
    for i in range(szvs):
        lift(ti, vs[i])
