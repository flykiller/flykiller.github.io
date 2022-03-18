from collections import deque
I = lambda: map(int, input().split())

n, m = I()
M = [input().rstrip() for _ in range(n)]

for i in range(n):
    for j in range(m):
        if M[i][j] == "A": A = (i, j)
        if M[i][j] == "B": B = (i, j)

Q = deque([(0, B[0], B[1])])
par = {B[0]*m + B[1]: -1}

while Q:
    d, x, y = Q.popleft()
    for dx, dy in (x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1):
        if not 0 <= dx < n or not 0 <= dy < m: continue
        if M[dx][dy] == "#" or dx*m + dy in par: continue
        Q.append((d + 1, dx, dy))
        par[dx*m + dy] = x*m + y

dirs = {1: "R", -1: "L", m: "D", -m: "U"}

if A[0]*m + A[1] in par:
    last, ans = A[0]*m + A[1], []
    path = [last]
    while last != B[0]*m + B[1]:
        ans += [dirs[par[last] - last]]
        last = par[last]
    print("YES")
    print(len(ans))
    print("".join(ans))
else:
    print("NO")