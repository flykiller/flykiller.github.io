from collections import deque
I = lambda: [int(i) for i in input().split()]

n = int(input())
pts = [tuple(I()) for _ in range(n)]
dist = {p: (-1, -1, int(1e9)) for p in pts}
d = [(-1, 0), (1, 0), (0, -1), (0, 1)]
Q = deque()

for i in range(n):
    ix, iy = pts[i]
    for dx, dy in d:
        nx = ix + dx
        ny = iy + dy
        if (nx, ny) not in dist:
            dist[(ix, iy)] = (nx, ny, 1)
            break
    if dist[(ix, iy)][2] == 1:
        Q.append((ix, iy))

while Q:
    x, y = Q.popleft()
    cx, cy, cd = dist[(x, y)]
    for dx, dy in d:
        nx = x + dx
        ny = y + dy
        if (nx, ny) in dist and cd + 1 < dist[(nx, ny)][2]:
            dist[(nx, ny)] = cx, cy, cd + 1
            Q.append((nx, ny))

for i in range(n):
    print(' '.join(map(str, dist[pts[i]][:2])))