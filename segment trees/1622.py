I = lambda: [int(x) for x in input().split()]
import sys

def q():
    val = int(input())
    return val

def p(v):
    print(v)
    sys.stdout.flush()

def eliminate(i1, i2, i3, i4):
    s1, s2, s3, s4 = str(i1), str(i2), str(i3), str(i4)
    V = []
    for i, x, y, z in (i1, s2, s3, s4), (i2, s1, s3, s4), (i3, s1, s2, s4), (i4, s1, s2, s3):
        p("? " + x + " " + y + " " + z)
        V += [(q(), i)]
    V = sorted(V)
    return V[-1][1], V[-2][1]

T = int(input())
for _ in range(T):
    n = int(input())
    indexes = list(range(1, n+1))
    while len(indexes) > 5:
        a, b = eliminate(*indexes[-4:])
        indexes.remove(a)
        indexes.remove(b)

    if len(indexes) == 5:
        a, _ = eliminate(*indexes[-4:])
        indexes.remove(a)

    a, b = eliminate(*indexes[-4:])
    indexes.remove(a)
    indexes.remove(b)

    p("! " + " ".join(str(x) for x in indexes) + "\n")