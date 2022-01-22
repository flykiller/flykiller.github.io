I = lambda: [int(i) for i in input().split()]

N, LOGN = 100100, 20
INF = float("inf")

n, m = I()
a = I()
q = []
for i in range(m):
    x, y = I()
    q += [(x-1, y, i)]


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
    szt = [0, 0]
    root[0] = newNode(0)
    root[1] = newNode(1)


def lift(ti, v):    #ti: trie number, v: node
    #if ti == 0:
    #    print("BEFORE", v, t0[v].maxv)
    tmp = t0 if ti == 0 else t1
    tmp[v].maxv = -INF
    for nv in tmp[v].nt:
        if nv != -1:
            print("INSIDE", tmp[nv].maxv)
            tmp[v].maxv = max(tmp[v].maxv, tmp[nv].maxv)

    #if ti == 0:
    #    print("AFTER", v, t0[v].maxv)



def calc(ti, x, minv):
    #print("CALC STARTED", ti, x, minv)
    v = root[ti]
    tmp = t0 if ti == 0 else t1
    if minv > tmp[v].maxv: return 0
    ans = 0
    for i in range(LOGN):
        d = (x >> i) & 1
        for jj in range(2):
            j = jj ^ d
            vv = tmp[v].nt[j]
            if vv != -1 and minv <= tmp[vv].maxv:
                v = tmp[v].nt[j]
                if jj: ans |= (1 << i)
                break
    print("ANS", ans)
    return ans


def add(ti, x, curv):
    v = root[ti]
    tmp = t0 if ti == 0 else t1
    szvs = 0
    vs = [0]*LOGN
    for i in range(LOGN):
        vs[szvs] = v
        szvs += 1
        d = (x >> i) & 1
        nt = tmp[v].nt[d]
        if nt == -1: nt = newNode(ti)
        v = nt

    tmp[v].maxv = max(tmp[v].maxv, curv)
    for i in range(szvs):
        lift(ti, vs[i])


def solve(l, r, rx):
    #print("HEREEE", l, r, rx)
    q[l:r] = sorted(q[l:r], key=lambda x: x[1])
    clear()
    print("AFTER CLEAR")
    px = rx
    cmax = 0
    for i in range(l, r):
        lf, rg, id = q[i]
        #print("HERE2", lf, rg, id, px)
        while px < rg:
            x = a[px]
            px += 1
            add(0, getXOR(x), x)
            cmax = max(cmax, calc(0, getXOR(x - 1), x))
            add(1, getXOR(x - 1), -x)
            cmax = max(cmax, calc(1, getXOR(x), -x))

        vmax = cmax
        #print("HERE3", lf, rg, rx)
        for j in range(lf, min(rg, rx)):
            x = a[j]
            vmax = max(vmax, calc(0, getXOR(x - 1), x))
            vmax = max(vmax, calc(1, getXOR(x), -x))

        ans[id] = max(ans[id], vmax)

    for i in range(l, r):
        lf, rg, id = q[i]
        rg = min(rg, rx)
        clear()
        cmax = 0
        for j in range(lf, rg):
            x = a[j]
            add(0, getXOR(x), x)
            cmax = max(cmax, calc(0, getXOR(x - 1), x))
            add(1, getXOR(x - 1), -x)
            cmax = max(cmax, calc(1, getXOR(x), -x))

        ans[id] = max(ans[id], cmax)

ans = [0] * m

q = sorted(q)

#print("QQQ", q)

i, j = 0, 0
S = 800   #change to root?

#print(n, S)

for lx in range(0, n, S):
    rx = min(n, lx + S)
    print("HERERE", rx)
    while j < m:
        if q[j][0] >= rx: break
        j += 1

    solve(i, j, rx)
    i = j

print(ans)
# print(szt, root)
# print(t0[0].nt)