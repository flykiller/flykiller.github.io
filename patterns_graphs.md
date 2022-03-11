---
layout: page
title: Patterns Graphs
permalink: /patterns/graphs
---

Here is a collection of different graph algorithms.


#### Floyd-Warshall
It will find the shortest paths between all pairs of nodes in $O(n^3)$ time, where $n$ is number of nodes. Sanity check here means that we have cycles with negative weigth.

```python
def floyd_warshall(n, edges):
    dist = [[0 if i == j else float("inf") for i in range(n)] for j in range(n)]
    pred = [[None] * n for _ in range(n)]

    for u, v, d in edges:
        dist[u][v] = d
        pred[u][v] = u

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    pred[i][j] = pred[k][j]
    """Sanity Check
    for u, v, d in edges:
        if dist[u] + d < dist[v]:
            return None
    """

    return dist, pred
```

#### Bellman-Ford algorithm
It will find shortest paths from given node to all others, if we can have negative weights, but not negative cycles. Time complexity is $O(mn)$, where $m$ is number of edges and $n$ is number of nodes. Sanity check again is used to find existance of negative loops.

```python
def bellman_ford(n, edges, start):
    dist = [float("inf")] * n
    pred = [None] * n

    dist[start] = 0

    for _ in range(n):
        for u, v, d in edges:
            if dist[u] + d < dist[v]:
                dist[v] = dist[u] + d
                pred[v] = u
    """Sanity Check
    for u, v, d in edges:
        if dist[u] + d < dist[v]:
            return None
    """

    return dist, pred
```

#### Strongly Connected Components, Tarjan

Here is Tarjan algorithm to detect strongly connected components in directed graph. Time and space complexity is $O(E+V)$ (however with quite big constant, like 5-7). Input is directed unweighted graph and output will be list of length $n$, where for each node we have index of SCC.

```python
from collections import defaultdict 
   
class Solution:       
    def SCCU_helper(self, u): 
        self.disc[u] = self.Time 
        self.low[u] = self.Time 
        self.Time += 1
        self.stackMember[u] = True
        self.st.append(u) 
        for v in self.graph[u]: 
            if self.disc[v] == -1 : 
                self.SCCU_helper(v) 
                self.low[u] = min(self.low[u], self.low[v])       
            elif self.stackMember[v] == True:  
                self.low[u] = min(self.low[u], self.disc[v]) 
  
        w = -1
        if self.low[u] == self.disc[u]: 
            while w != u: 
                w = self.st.pop() 
                self.comp[w] = u
                self.stackMember[w] = False

    def SCC(self, n, connections):
        self.Time = 0
        self.disc = [-1] * n   #discovery time
        self.low = [-1] * n    #low link
        self.stackMember = [False] * n 
        self.st = []
        self.comp = [-1]*n     #component number for each node
        self.graph = defaultdict(list)

        for u, v in connections:
            self.graph[u].append(v)

        for i in range(n): 
            if self.disc[i] == -1: 
                self.SCCU_helper(i) 

        return self.comp
```

#### Strongly Connected Components, Kosaraju
Here is Kosaraju algorithm to evaluate strongly connected components in graph, complexity is also $O(V + E)$.
It will return two pieces of information:
1. `SCC` is list of lists, where in each list we have stronlgy connected component and these components follow the topological sort of graph with components merged to point.
2. `out` is list of length `n`, where for each node we have index of connected component.

```python
def kosaraju(G, n):
    SCC, S, P, out, D = [], [], [], [0]*n, [0]*n
    st = list(range(n))
    
    while st:
        x = st.pop()
        if x < 0:
            d = D[~x] - 1
            if P[-1] > d:
                SCC += [S[d:]]
                del S[d:], P[-1]
                for x in SCC[-1]: D[x] = -1
        elif D[x] > 0:
            while P[-1] > D[x]: P.pop()
        elif D[x] == 0:
            S += [x]
            P += [len(S)]
            D[x] = len(S)
            st += [~x]
            st += G[x]

    for x, comp in enumerate(SCC):
        for i in comp: out[i] = x
    return SCC[::-1], out
```

#### Dijkstra Algorithm

Let $n$ be number of nodes with numbers $0,1,\dots, n-1$ and `edges` be edges in form: `from, to, weight`. Let `start` and `end` be nodes between which we want to find minimal distance. Time complexity is $O((E+V)\log V)$, space complexity is $O(E+V)$.

```python
from heapq import heappop, heappush
from collections import defaultdict

class Solution:
    def Dijkstra(self, n, edges, start, end):
        dist = [float('inf')] * n
        dist[start] = 0
        G = defaultdict(list)
        
        for a, b, w in edges:
            G[a].append((b, w))
            G[b].append((a, w))
        
        heap = [(0, start)]

        while heap:
            (min_dist, id) = heappop(heap)
            if id == end: return min_dist
            for neibh, weight in G[id]:
                cand = min_dist + weight
                if cand < dist[neibh]:
                    dist[neibh] = cand
                    heappush(heap, (cand, neibh))
                    
        return -1
````

#### Bridges
Bridges partition graph into biconnected edge components, goal is to find all bridges in graph in $O(V + E)$ time.

```python
class Solution:
    def criticalConnections(self, n, connections):
        used, tin, fup = [0]*n, [-1]*n, [-1]*n
        self.timer, ans = 0, []
        graph = defaultdict(list)
        
        def dfs(node, par = -1):
            used[node] = 1
            tin[node] = fup[node] = self.timer + 1
            self.timer += 1
            for child in graph[node]:
                if child == par: continue
                if used[child] == 1:
                    fup[node] = min(fup[node], tin[child])
                else:
                    dfs(child, node)
                    fup[node] = min(fup[node], fup[child])
                    if fup[child] > tin[node]: ans.append([node, child])
        
        for i, j in connections:
            graph[i].append(j)
            graph[j].append(i)
            
        for i in range(n):
            if not used[i]: dfs(i)
                
        return ans
```

See also leetcode 1192.


#### Articulation points
**Articulation points** in graphs: such points which being removed break graph into parts. Articulation points partition graph into biconnected vertex components. Here is implementation of classical algorithm. Note that it is very similar to bridges with small differences:

1. It is `fup[child] >= tin[node]` instead of `fup[child] > fup[node]`.
2. We also keep `children`: number of connections and make one more check if `par = -1` and number of children more than one (it means, they can not have common descendents), then this is also articulation point.
3. Finally, we keep set of articulation points, not list, because one node can be visited several times during traversal.

```python
class Solution:
    def ArticulationPoints(self, n, connections):
        used, tin, fup = [0]*n, [-1]*n, [-1]*n
        self.timer, ans = 0, set()
        graph = defaultdict(list)
        
        def dfs(node, par = -1):
            used[node] = 1
            tin[node] = fup[node] = self.timer + 1
            self.timer += 1
            children = 0
            for child in graph[node]:
                if child == par: continue
                if used[child] == 1:
                    fup[node] = min(fup[node], tin[child])
                else:
                    dfs(child, node)
                    fup[node] = min(fup[node], fup[child])
                    if fup[child] >= tin[node] and par != -1: ans.add(node)
                    children += 1

            if par == -1 and children > 1: ans.add(node)
        
        for i, j in connections:
            graph[i].append(j)
            graph[j].append(i)
            
        for i in range(n):
            if not used[i]: dfs(i)
                
        return ans
```

See also problem **0928**, where one of the solutions can use this idea.

#### Topological sort

Given graph, check if it is DAG, and if it is, give the correct order of nodes, if not, return $[]$. Here is code which use BFS, time and space complexity is $O(V + E)$. `verts` is list of vertices and `E` is list of edges.
```python
def Topological(verts, edges):
    pre, suc = defaultdict(int), defaultdict(list)
    for a, b in edges:
        pre[a] += 1
        suc[b].append(a)

    free, out = set(verts) - set(pre), []
    while free:
        a = free.pop()
        out.append(a)
        for b in suc[a]:
            pre[b] -= 1
            if not pre[b]: free.add(b)
    return out * (len(out) == len(verts))
```

#### Euler path
Given edges of graph, return euler path. Time complexity is `O(E + V)`.
Notice that graph is oriented, so it is general case.

```python
def Euler(pairs):
    G = defaultdict(list)
    D = Counter() # net out degree 
    for x, y in pairs: 
        G[x].append(y)
        D[x], D[y] = D[x] + 1, D[y] - 1

    for k in D: 
        if D[k] == 1: 
            x = k
            break 

    ans, stack = [], [x]
    while stack: 
        while G[stack[-1]]: 
            stack.append(G[stack[-1]].pop())
        ans.append(stack.pop())
    return ans[::-1]
```

#### Bipartite graphs
We can check if graph is bipartite, using usual dfs: either recursive or with stack. With stack it is faster. Time complexity is `O(E + V)`.
The result is `color`, where `color[i]` is 0 or 1 depending on part of graph.

```python
def is_bipartite(graph):
    n = len(graph)
    color = [-1] * n

    for start in range(n):
        if color[start] == -1:
            color[start] = 0
            stack = [start]

            while stack:
                parent = stack.pop()

                for child in graph[parent]:
                    if color[child] == -1:
                        color[child] = 1 - color[parent]
                        stack.append(child)
                    elif color[parent] == color[child]:
                        return False, color

    return True, color
```

#### BFS
Classical bfs implementation: given graph and starting node, we traverse it with bfs.

Function `layers` will return layers, where in first layer distance is `0`, then distance is `1` and so on.

```python
def bfs(graph, start=0):
    used = [False] * len(graph)
    used[start] = True
    q = [start]
    for v in q:
        for w in graph[v]:
            if not used[w]:
                used[w] = True
                q.append(w)


def layers(graph, start=0):
    used = [False] * len(graph)
    used[start] = True
    q, ret = [start], []
    while q:
        nq = []
        ret.append(q)
        for v in q:
            for w in graph[v]:
                if not used[w]:
                    used[w] = True
                    nq.append(w)
        q = nq
    return ret
```

#### Bidirectional BFS
We can use bidirectional bfs in the cases, where we need to find the shortest path between nodes `beg` and `end`.
The idea is to start from both ends and each time choose the end with smaller size of queue. Here we need to be careful: Our invariant, that at each moment of time in our queues we have number of steps (first elements):

`[i,i,..., i, i+1, i+1, ..., i+1]` and `[j,j,..., j, j+1, j+1, ..., j+1]`

We extract left element from first queue and we need to check if it is in second. At this moment we for sure know that distance is not more than i + j. However, it can be either i+j or i+j+1, and we need to check all elements with length i to make sure there is no element from second queue with steps `j`. So, first time we see that sum of first elements from our queue is more than limit, it means that we finished to process all candidates, so we can return answer.

Also I add empty the part where we look for all neibhours of node `cand`. Usually for bidirectional bfs it makes sense not to construct the whole graph (if we have it, why not just use usual bfs), but we construct connections only if needed: on the fly. So, instead of line `neibs = ???` you need to create list of all possible neibhours.

Complexity is potentially as in bfs, but for some graphs it works much better, especially if distance is not very big.

**Use with care, code is not full and not fully tested**

```python
def bfs_bidir(beg, end):
    queue1 = deque([(0, beg)])
    queue2 = deque([(0, end)])
    visited1 = {beg: 0}
    visited2 = {end: 0}

    limit, ans = float("inf"), float("inf")

    while queue1:
        if len(queue1) > len(queue2):
            queue1, queue2 = queue2, queue1
            visited1, visited2 = visited2, visited1

        steps, elem, = queue1.popleft()
        if steps + queue2[0][0] > limit: return ans

        if elem in visited2:
            limit = steps + queue2[0][0]
            ans = min(visited1[code] + visited2[code], ans)
    
        neibs = ???   #list of all neibs of elem
        for cand in neibs:
            if cand not in visited1:
                visited1[cand] = step + 1
                queue1.append((steps + 1, cand))
    return -1
```

#### LCA
Given tree, the goal is to answer queries: find LCA of two given nodes. There are at least two different approaches to solve this problem:

1.1 First way is to use Eulerian traversal of graph and then use segment tree/sparse table to answer queries.
Also we need `indxs` array\dict where for each value we keep the last occurence of this node (in fact we can keep any occurence, but it is easy to code for the last one).
**full code not tested here**


```python
self.arr, self.dep = [], []  #euler path
def dfs(node, depth):
    self.arr += [node]
    self.dep += [depth]
    for child in filter(None, [node.left, node.right]):
        dfs(child, depth + 1)
        self.arr += [node]
        self.dep += [depth]

dfs(root, 0)
indxs = {x:i for i, x in enumerate(self.arr)}
```

1.2 Another way is to use dfs, where for each node we keep the time when we extracted this node from dfs stack. I think it is more or less equivalent to the previous approach.

```python
class RangeQuery:
    def __init__(self, data, func=min):
        self.func = func
        self._data = _data = [list(data)]
        i, n = 1, len(_data[0])
        while 2 * i <= n:
            prev = _data[-1]
            _data.append([func(prev[j], prev[j + i]) for j in range(n - 2 * i + 1)])
            i <<= 1

    def query(self, begin, end):
        depth = (end - begin).bit_length() - 1
        return self.func(self._data[depth][begin], self._data[depth][end - (1 << depth)])


class LCA:
    def __init__(self, root, graph):
        self.time = [-1] * len(graph)
        self.path = [-1] * len(graph)
        P = [-1] * len(graph)
        t = -1
        dfs = [root]
        while dfs:
            node = dfs.pop()
            self.path[t] = P[node]
            self.time[node] = t = t + 1
            for nei in graph[node]:
                if self.time[nei] == -1:
                    P[nei] = node
                    dfs.append(nei)
        self.rmq = RangeQuery(self.time[node] for node in self.path)

    def __call__(self, a, b):
        if a == b:
            return a
        a = self.time[a]
        b = self.time[b]
        if a > b:
            a, b = b, a
        return self.path[self.rmq.query(a, b)]
```

2.0 Use binary lyfting, see Leetcode 1724 solution for more details.

#### Hungarian algorithm
Given `n x n` matrix the goal is to choose such `n` cells, no two of them lies in the same line or row such that sum of given cells is **maximized**
Here is so-called hungarian algorighm with time complexity `O(n^3)`. The result will be total sum and coordinates of cells.

```python
def hungarian(G, T=1e-6):
    n = len(G)
    U, V = range(n), range(n)
    mu, mv = [None] * n, [None] * n
    lu = [max(row) for row in G]
    lv = [0] * n
    for root in U:
        au = [False] * n
        au[root] = True
        Av = [None] * n
        slack = [(lu[root] + lv[v] - G[root][v], root) for v in V]
        while True:
            (delta, u), v = min((slack[v], v) for v in V if Av[v] == None)
            if delta > T:
                for u0 in U:
                    if au[u0]: lu[u0] -= delta
                for v0 in V:
                    if Av[v0] != None: lv[v0] += delta
                    else:
                        (val, arg) = slack[v0]
                        slack[v0] = (val - delta, arg)

            Av[v] = u
            if mv[v] == None: break
            u1 = mv[v]
            au[u1] = True
            for v1 in V:
                if Av[v1] == None:
                    slack[v1] = min((lu[u1] + lv[v1] - G[u1][v1], u1), slack[v1])
        while v != None:
            u = Av[v]
            prec = mu[u]
            mv[v] = u
            mu[u] = v
            v = prec
    return (mu, sum(lu) + sum(lv))
```

#### Maximum bipartite matching

Given bipartite graph `G`, the goal is to find the maximum bipartite matching. We can do it in `O(E * n)` time. Output will be list, where for each node we have `None` if it is not in partitioning and node if it is. For example for graph with parts `{0, 1, 2, 3}` and `{4, 5, 6}`, where we have edges `(0, 5), (1, 5), (2, 4), (2, 6), (3, 6)` one of the possible answers is `[5, None, 4, 6, 2, 0, 3]`, meaning that we found edges `(0, 5), (2, 4), (3, 6)`.

```python
def dfs(u, G, V, match):
    for v in G[u]:
        if not V[v]:
            V[v] = True
            if match[v] is None or dfs(match[v], G, V, match):
                match[v] = u
                return True
    return False

def max_bipartite_matching(G):
    n = len(G)
    match = [None] * n
    for u in range(n):
        dfs(u, G, [False] * n, match)
    return match
```

