I = lambda: [int(i) for i in input().split()]

N, LOGN = 100100, 4   #CHANGE
INF = float("inf")

n, m = I()
a = I()
q = []
for idx in range(m):
    x, y = I()
    q += [(x-1, y, idx)]


def getXOR(a):
    return [a, 1, a+1, 0][a%4]


class Node:
    def __init__(self, nt=(-1, -1), maxv=-INF):
        self.nt = nt
        self.maxv = maxv

root = [0, 0]
szt = [0, 0]
t0, t1 = [Node()]*(N * LOGN), [Node()]*(N * LOGN)


def newNode(i):
    tmp = t0 if i == 0 else t1
    tmp[szt[i]] = Node()
    szt[i] += 1
    return szt[i] - 1


def clear():
    for i in range(2):
        szt[i] = 0
        root[i] = newNode(i)


def lift(ti, v):    #ti: trie number, v: node
    tmp = t0 if ti == 0 else t1
    tmp[v].maxv = -INF
    for nv in tmp[v].nt:
        if nv != -1:
            tmp[v].maxv = max(tmp[v].maxv, tmp[nv].maxv)



def calc(ti, x, minv):
    v = root[ti]
    tmp = t0 if ti == 0 else t1
    if minv > tmp[v].maxv: return 0
    ans = 0
    for i in range(LOGN-1, -1, -1):
        d = (x >> i) & 1
        for jj in range(1, -1, -1):
            j = jj ^ d
            vv = tmp[v].nt[j]
            if vv != -1 and minv <= tmp[vv].maxv:
                v = tmp[v].nt[j]
                if jj: ans |= (1 << i)
                break
    return ans


def add(ti, x, curv):
    print("HERE ADD", ti, x, curv)
    v = root[ti]
    tmp = t0 if ti == 0 else t1
    szvs = 0
    vs = [0]*LOGN
    for i in range(LOGN-1, -1, -1):
        print("v", v)
        vs[szvs] = v
        szvs += 1
        d = (x >> i) & 1
        nt = tmp[v].nt[d]
        if nt == -1: nt = newNode(ti)
        v = nt

    tmp[v].maxv = max(tmp[v].maxv, curv)
    print("CURV", curv, tmp[v].maxv)
    for i in range(szvs-1, -1, -1):
        lift(ti, vs[i])


def solve(l, r, rx):
    q[l:r] = sorted(q[l:r], key=lambda x: x[1])
    clear()

    px = rx
    cmax = 0
    for i in range(l, r):
        lf, rg, idx = q[i]
        while px < rg:
            x = a[px]
            px += 1
            add(0, getXOR(x), x)
            cmax = max(cmax, calc(0, getXOR(x - 1), x))
            add(1, getXOR(x - 1), -x)
            cmax = max(cmax, calc(1, getXOR(x), -x))

        vmax = cmax
        for j in range(lf, min(rg, rx)):
            x = a[j]
            vmax = max(vmax, calc(0, getXOR(x - 1), x))
            vmax = max(vmax, calc(1, getXOR(x), -x))

        ans[idx] = max(ans[idx], vmax)

    for i in range(l, r):
        lf, rg, idx = q[i]
        rg = min(rg, rx)
        clear()
        cmax = 0
        for j in range(lf, rg):
            x = a[j]
            add(0, getXOR(x), x)
            cmax = max(cmax, calc(0, getXOR(x - 1), x))
            add(1, getXOR(x - 1), -x)
            cmax = max(cmax, calc(1, getXOR(x), -x))

        ans[idx] = max(ans[idx], cmax)

    print("ANS", ans)

ans = [0] * m

q = sorted(q)

i2, j = 0, 0
S = 800   #change to root?

for lx in range(0, n, S):
    rx = min(n, lx + S)
    while j < m:
        if q[j][0] >= rx: break
        j += 1

    solve(i2, j, rx)
    i2 = j

print(ans)