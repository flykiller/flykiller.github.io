---
layout: page
title: Patterns Data Structures
permalink: /patterns/data structures
---

Here is a collection of different data structures patterns.


#### Bit array
Implements bitarray using bytearray. If you have a lot of 0/1 data that there is very compact way to keep it it in bitarray, which will take `8` less space than `bytearray` and `32` times less than list of integers.

```python
class BitArray:
    def __init__(self, size):
        self.bytes = bytearray((size >> 3) + 1)

    def __getitem__(self, index):
        return (self.bytes[index >> 3] >> (index & 7)) & 1

    def __setitem__(self, index, value):
        if value:
            self.bytes[index >> 3] |= 1 << (index & 7)
        else:
            self.bytes[index >> 3] &= ~(1 << (index & 7))
```

#### Binary indexed tree
This data structure is less flexible than segment trees, but much more easier to code. Here is implemenation to have queries of sums of numbers in the form `[0, i]`, also it is easy to do ranges `[i, j]`. We can choose another function (which what properties?), such that we only can answer `[0, i]` queries, for example to evaluate `max`.

```python
class BIT:
    def __init__(self, n):
        self.sums = [0] * (n+1)
    
    def update(self, i, delta):
        while i < len(self.sums):
            self.sums[i] += delta
            i += i & (-i)
    
    def query(self, i):
        res = 0
        while i > 0:
            res += self.sums[i]
            i -= i & (-i)
        return res

    def sum(self, i, j):
        return self.query(j) - self.query(i-1)
```

##### advanced version.
1. `__init__(self, x)` will transform list `x` to BIT in `O(n)` time.
2. `update(self, idx, x)` will update `bit[idx] += x` in `O(log n)` time.
3. `query(self, i)` will calculate `sum(bit[:i])`, be careful here, `i` is not included in `O(log n)` time
4. `findkth(self, k)` find largest `idx` such that `sum(bit[:idx]) <= k` in `O(log^2 n) time).

```python
class BIT
    def __init__(self, x):
        self.bit = x
        for i in range(len(x)):
            j = i | (i + 1)
            if j < len(x):
                x[j] += x[i]

    def update(self, idx, x):
        while idx < len(self.bit):
            self.bit[idx] += x
            idx |= idx + 1

    def query(self, i):
        x = 0
        while i:
            x += self.bit[i - 1]
            i &= i - 1
        return x

    def findkth(self, k):
        idx = -1
        for d in reversed(range(len(self.bit).bit_length())):
            right_idx = idx + (1 << d)
            if right_idx < len(self.bit) and k >= self.bit[right_idx]:
                idx = right_idx
                k -= self.bit[idx]
        return idx + 1
```

#### Fractions
In python there is library which works with fractions already, but is quite slow. If you want faster implementation, here it is.

Also, there is `limit_denominator(frac, max_den)` function, which is given fraction and maximum denominator, will find the closest fraction with denominator which is less or equal to maximum denominator. Complexity I think is logarithmic.

```python
class Fraction:
    def __init__(self, num=0, den=1):
        g = gcd(num, den)
        self.num, self.den = num // g, den // g

    __add__ = lambda self, other: Fraction(self.num * other.den + other.num * self.den, self.den * other.den)
    __sub__ = lambda self, other: Fraction(self.num * other.den - other.num * self.den, self.den * other.den)
    __mul__ = lambda self, other: Fraction(self.num * other.num, self.den * other.den)
    __truediv__ = lambda self, other: Fraction(self.num * other.den, self.den * other.num)
    __floordiv__ = lambda self, other: (self.num * other.den) // (self.den * other.num)

    __pow__ = lambda self, other: Fraction(self.num**other, self.den**other)
    __abs__ = lambda self: self if self.num >= 0 else Fraction(-self.num, self.den)
    __neg__ = lambda self: Fraction(-self.num, self.den)
    __round__ = lambda self, ndigits: round(self.num / self.den, ndigits)

    __bool__ = lambda self: bool(self.num)
    __int__ = lambda self: self.num // self.den
    __float__ = lambda self: self.num / self.den
    __str__ = lambda self: "({}, {})".format(self.num, self.den)

    __copy__ = lambda self: Fraction(self.num, self.den)
    __hash__ = lambda self: hash((self.num, self.den))

    __eq__ = lambda self, other: self.num * other.den == other.num * self.den
    __ne__ = lambda self, other: self.num * other.den != other.num * self.den
    __lt__ = lambda self, other: self.num * other.den < other.num * self.den
    __gt__ = lambda self, other: self.num * other.den > other.num * self.den
    __le__ = lambda self, other: self.num * other.den <= other.num * self.den
    __ge__ = lambda self, other: self.num * other.den >= other.num * self.den

    __repr__ = lambda self: "Fraction({}, {})".format(self.num, self.den)


def limit_denominator(frac, max_den=1000000):
    if frac.den <= max_den:
        return frac

    p0, q0, p1, q1 = 0, 1, 1, 0
    n, d = frac.num, frac.den
    while True:
        a = n // d
        q2 = q0 + a * q1
        if q2 > max_den:
            break
        p0, q0, p1, q1 = p1, q1, p0 + a * p1, q2
        n, d = d, n - a * d

    k = (max_den - q0) // q1
    bound1 = Fraction(p0 + k * p1, q0 + k * q1)
    bound2 = Fraction(p1, q1)
    return bound2 if abs(bound2 - frac) <= abs(bound1 - frac) else bound1
```

#### Continuous fractions
1. `CFraction(frac)` transforms usual franction to continuous fraction, e.g. `123/32 -> 3, 1, 5, 2, 2`.
2. `CFrac2Frac(cfrac)` transforms in the opposite direction.

```python
def CFraction(frac):
    num, den = frac
    yield num // den
    num %= den
    while den != 1:
        num, den = den, num
        yield num // den
        num %= den

def CFrac2Frac(cfrac):
    num, den = 1, 0
    for u in reversed(cfrac):
        num, den = den + num * u, num
    return (num, den)
```

#### Union find

##### Version 1

Note, that `self.p` is **not** values of set for each node, but pointer to parent.

Without ranks implementation but with path compression. It has potentially $O(n)$ time complexity, but in practice, if data is not meant to broke it will work like $O(\log n)$ in average.
```python
class DSU:
    def __init__(self, N):
        self.p = list(range(N))

    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def union(self, x, y):
        xr = self.find(x)
        yr = self.find(y)
        self.p[xr] = yr
```

##### Version 2
If previous implementation is not enough, there is implementation with ranks and with path compressions, which will be $O(\mathcal{A}(n))$ complexity, where $\mathcal{A}(n)$ is inverse Ackermann funcion, which in fact grows so slow, that we can state that complexity is $O(1)$. Actually path compressions will make code just one line longer.

```python
class DSU(object):
    def __init__(self, N):
        self.par = list(range(N))
        self.rnk = [0] * N

    def find(self, x):
        if self.par[x] != x:
            self.par[x] = self.find(self.par[x])
        return self.par[x]

    def union(self, x, y):
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return False
        elif self.rnk[xr] < self.rnk[yr]:
            self.par[xr] = yr
        elif self.rnk[xr] > self.rnk[yr]:
            self.par[yr] = xr
        else:
            self.par[yr] = xr
            self.rnk[xr] += 1
        return True
```

##### Version 3
If you need a bit more functionality, use this version: here we have also have size of each set (however we do not have ranks) and we have total number of sets.

```python
class DisjointSetUnion:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.num_sets = n

    def find(self, a):
        acopy = a
        while a != self.parent[a]:
            a = self.parent[a]
        while acopy != a:
            self.parent[acopy], acopy = a, self.parent[acopy]
        return a

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a != b:
            if self.size[a] < self.size[b]:
                a, b = b, a

            self.num_sets -= 1
            self.parent[b] = a
            self.size[a] += self.size[b]

    def set_size(self, a):
        return self.size[self.find(a)]

    def __len__(self):
        return self.num_sets
```

#### Linked list
`Node` is just definition for double linked list node. Now, let us discuss `LinkedList` functions:

1. `__init__` is just initialize empty double linked list, which is looped: that is last node connected to the first. Sentinel node do not have value and have `None` inside.
2. `get_node(self, index)` will return node given `index`. Also if we reached the end it will return `None`.
3. `__getitem__(self, index)` will return value of node given index.
4. `__len__(self)` is length of our linked list.
5. `__setitem__(self, index, value)` will update node at `index` with new `value`.
6. `__delitem__(self, index)` will delete node in given index if it is possible.
7. `__repr__(self)` is to show what is inside our list.
8. `to_list(self)` is to transform our linked list to usual list.
9. `append(self, value)` is to append new node to the end.
10. `appendleft(self, value)` is to append new node to the start.
11. `insert(self, index, value)` is to insert new value at given index.
12. `insert_between(self, node, left_node, right_node)` is to insert new node between two nodes.
13. `insert_after(self, node, value)` is to insert node after given node. Different with `insert` is that here we have node, not index.
14. `merge_left(self, other)` is to concatenate new list to the left of the current list.
15. `merge_right(self, other)`, similar but from the right.
16. `pop(self, node = None)` is to delete node if possible and return its value.
17. `before` is return node before if possible, if not, return cycle shift.
18. `after is to return node after node if possible and if not, return cycle shift.


```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

    def __repr__(self):
        if not self:
            return "{}()".format(self.__class__.__name__)
        return "{}({})".format(self.__class__.__name__, self.value)


class LinkedList:
    def __init__(self, iterable=None):
        self.sentinel = Node(None)
        self.sentinel.next = self.sentinel
        self.sentinel.prev = self.sentinel
        self.__len = 0
        if iterable is not None:
            self += iterable

    def get_node(self, index):
        node = self.sentinel
        i = 0
        while i <= index:
            node = node.next
            if node == self.sentinel:
                break
            i += 1
        if node == self.sentinel:
            node = None
        return node

    def __getitem__(self, index):
        node = self.get_node(index)
        return node.value

    def __len__(self):
        return self.__len

    def __setitem__(self, index, value):
        node = self.get_node(index)
        node.value = value

    def __delitem__(self, index):
        node = self.get_node(index)
        if node:
            node.prev.next = node.next
            if node.next:
                node.next.prev = node.prev
            node.prev = None
            node.next = None
            node.value = None
            self.__len -= 1

    def __repr__(self):
        return str(self.to_list())

    def to_list(self):
        elts = []
        curr = self.sentinel.next
        while curr != self.sentinel:
            elts.append(curr.value)
            curr = curr.next
        return elts

    def append(self, value):
        node = Node(value)
        self.insert_between(node, self.sentinel.prev, self.sentinel)

    def appendleft(self, value):
        node = Node(value)
        self.insert_between(node, self.sentinel, self.sentinel.next)

    def insert(self, index, value):
        new_node = Node(value)
        len_ = len(self)
        if len_ == 0:
            self.insert_between(new_node, self.sentinel, self.sentinel)
        elif index >= 0 and index < len_:
            node = self.get_node(index)
            self.insert_between(new_node, node.prev, node)
        elif index == len_:
            self.insert_between(new_node, self.sentinel.prev, self.sentinel)
        else:
            raise IndexError

    def insert_between(self, node, left_node, right_node):
        if node and left_node and right_node:
            node.prev = left_node
            node.next = right_node
            left_node.next = node
            right_node.prev = node
            self.__len += 1
        else:
            raise IndexError

    def insert_after(self, node, value):
        new_node = Node(value)
        node.next.prev = new_node
        new_node.next = node.next
        node.next = new_node
        new_node.prev = node
        self.__len += 1

    def merge_left(self, other):
        self.sentinel.next.prev = other.sentinel.prev
        other.sentinel.prev.next = self.sentinel.next
        self.sentinel.next = other.sentinel.next
        self.sentinel.next.prev = self.sentinel
        self.__len += other.__len

    def merge_right(self, other):
        self.sentinel.prev.next = other.sentinel.next
        other.sentinel.next.prev = self.sentinel.prev
        self.sentinel.prev = other.sentinel.prev
        self.sentinel.prev.next = self.sentinel
        self.__len += other.__len

    def pop(self, node = None):
        if node == None:
            node = self.sentinel.prev
        if self.__len < 1:
            raise IndexError
        node.prev.next = node.next
        node.next.prev = node.prev
        self.__len -= 1
        return node.value

    def before(self, node):
        if node.prev == self.sentinel:
            return node.prev.prev
        return node.prev

    def after(self, node):
        if node.next == self.sentinel:
            return node.next.next
        return node.next
```

#### Sparse table
It is used to answer queries on range in `O(1)` given function `min, max` or another function such that `f(x, x) = x`. Time of construction is `O(n log n)`, time of query is `O(1)`.

Notice, that Minimum Range Query problem can be solved in different ways, the best init/range complexity is `O(n)/O(1)`, but it is quite difficult to code (**ADD TEMPLATE**)

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

    def query(self, start, stop):
        """func of data[start, stop)"""
        depth = (stop - start).bit_length() - 1
        return self.func(self._data[depth][start], self._data[depth][stop - (1 << depth)])

    def __getitem__(self, idx):
        return self._data[0][idx]
```

#### Segment Tree with lazy updates
There are different versions of segment trees with different funcionality.

##### Version 1
Here is universal Segment Tree with $O(\log n)$ complexities of each operation. What we need here is to be able to have the following data structure. Given numbers $x_1,\dots, x_n$, we want:
1. Find maximum (or another function `query_fn`, properties will be discussed later) on range `[l, r]`, this is query(self, v, tl, tr, l, r) and we want to do it in $O(\log n)$ complexity. We need to run it with arguments `(1, 0, n-1, l, r)` to get answer on range `[l, r]`. Here `v` is index of segment, `1` corresponds to range `[0, n-1]` and each segment have two children with indexes `2*v` and `2*v+1`, that is why we start indexing with `1`, not `0`.
2. Update values for whole range `[l, r]`, using function `update_fn`. Note, that it is more difficult, that just to update one value, and we need to use so-called lazy updates. This is function `update(self, v, tl, tr, l, r, h)` We need to run it with arguments `(1, 0, n-1, l, r, h)`. Time complexity is also $O(\log n)$.

Now, let us discuss possible choices of query and update functions. Denote `update_fn` by $\otimes$ and `query_fn` by $\oplus$, then they should have the following properties:
1. We have semigroup for binary operation $\oplus$: $(a\oplus b)\oplus c = a\oplus (b\oplus c); $
2. We have monoid for binary operation $\otimes$:  $(a\otimes b)\otimes c = a\otimes (b\otimes c)$, $a\otimes e = e\otimes a = a$
3. $\otimes$ is right-distributive over $\oplus$: $(a\otimes c)\oplus (b\otimes c) = (a\oplus b) \otimes c$

Note also, that we can easily create so-called sparse segment tree: instead of list with zeroes, we can keep dictionary. Then space complexity for whole tree will be $O(k\log N)$ instead of $O(N)$, where $k$ is number of elements in tree.

Here is iterative version, which in practice works 1.5-2 times faster than recursive. **Be carefull with zero elements**, they will change depending on `update_fn` and `query_fn`.

```python
class SegmentTree:
    def __init__(self, N, update_fn, query_fn):
        self.N = N
        self.H = 1
        while 1 << self.H < N:
            self.H += 1

        self.update_fn = update_fn
        self.query_fn = query_fn
        self.tree = [0] * (2 * N)
        self.lazy = [0] * N

    def _apply(self, x, val):
        self.tree[x] = self.update_fn(self.tree[x], val)
        if x < self.N:
            self.lazy[x] = self.update_fn(self.lazy[x], val)

    def _pull(self, x):
        while x > 1:
            x /= 2
            self.tree[x] = self.query_fn(self.tree[x*2], self.tree[x*2 + 1])
            self.tree[x] = self.update_fn(self.tree[x], self.lazy[x])

    def _push(self, x):
        for h in xrange(self.H, 0, -1):
            y = x >> h
            if self.lazy[y]:
                self._apply(y * 2, self.lazy[y])
                self._apply(y * 2+ 1, self.lazy[y])
                self.lazy[y] = 0

    def update(self, L, R, h):
        L += self.N
        R += self.N
        L0, R0 = L, R
        while L <= R:
            if L & 1:
                self._apply(L, h)
                L += 1
            if R & 1 == 0:
                self._apply(R, h)
                R -= 1
            L /= 2; R /= 2
        self._pull(L0)
        self._pull(R0)

    def query(self, L, R):
        L += self.N
        R += self.N
        self._push(L); self._push(R)
        ans = 0
        while L <= R:
            if L & 1:
                ans = self.query_fn(ans, self.tree[L])
                L += 1
            if R & 1 == 0:
                ans = self.query_fn(ans, self.tree[R])
                R -= 1
            L /= 2; R /= 2
        return ans
```

##### Version 2
It is recursive version of previous algorithm. Again be carefull with zero elements.

```python
class SegmentTree:
    def __init__(self, N, update_fn, query_fn):
        self.UF, self.QF = update_fn, query_fn
        self.T = defaultdict(int)   # [0] * (4*N)
        self.L = defaultdict(int)   # [0] * (4*N)
    
    def push(self, v):
        for u in [2*v, 2*v+1]:
            self.T[u] = self.UF(self.T[u], self.L[v])
            self.L[u] = self.UF(self.L[u], self.L[v])
        self.L[v] = 0

    def update(self, v, tl, tr, l, r, h):
        if l > r: return
        if l == tl and r == tr:
            self.T[v] = self.UF(self.T[v], h)
            self.L[v] = self.UF(self.L[v], h)
        else:
            self.push(v)
            tm = (tl + tr)//2
            self.update(v*2, tl, tm, l, min(r, tm), h)
            self.update(v*2+1, tm+1, tr, max(l, tm+1), r, h)
            self.T[v] = self.QF(self.T[v*2], self.T[v*2+1])

    def query(self, v, tl, tr, l, r):
        if l > r: return -float("inf")
        if l <= tl and tr <= r: return self.T[v]
        self.push(v)
        tm = (tl + tr)//2
        return self.QF(self.query(v*2, tl, tm, l, min(r, tm)), self.query(v*2+1, tm+1, tr, max(l, tm+1), r))
```

##### Version 3
Here is lighter version, which works faster, but without range updates.

```python
class SegmentTree:
    def __init__(self, update_fn, query_fn):
        self.UF, self.QF = update_fn, query_fn
        self.T = defaultdict(int)  

    def update(self, v, tl, tr, pos, h):
        if tl == tr: 
            self.T[v] = self.UF(self.T[v], h)
        else:
            tm = (tl + tr)//2
            if pos <= tm:
                self.update(v*2, tl, tm, pos, h)
            else:
                self.update(v*2+1, tm+1, tr, pos, h)
            self.T[v] = self.QF(self.T[v*2], self.T[v*2+1])

    def query(self, v, tl, tr, l, r):
        if l > r: return 0
        if l == tl and r == tr: return self.T[v]
        tm = (tl + tr)//2
        return self.QF(self.query(v*2, tl, tm, l, min(r, tm)), self.query(v*2+1, tm+1, tr, max(l, tm+1), r))
```


#### Persistent Segment Tree
I think it is quite rare: see for code <a href="https://github.com/cheran-senthil/PyRival/blob/master/pyrival/data_structures/PersistentSegTree.py"> <font color = blue>https://github.com/cheran-senthil/PyRival/blob/master/pyrival/data_structures/PersistentSegTree.py/


The idea of this tree that it keeps changes.

#### Sorted List
If it is allowed to import it, just import. If not, copy code from <a href="https://github.com/cheran-senthil/PyRival/blob/master/pyrival/data_structures/SortedList.py"> <font color = blue>https://github.com/cheran-senthil/PyRival/blob/master/pyrival/data_structures/SortedList.py

#### Treap
Another data structure with the same complexities as SortedList, check <a href="https://github.com/cheran-senthil/PyRival/blob/master/pyrival/data_structures/Treap.py
"> <font color = blue>https://github.com/cheran-senthil/PyRival/blob/master/pyrival/data_structures/Treap.py

#### Trie

##### Version 1
Here is implementation of trie, it is not the shortest one, but in this way you can modify it easily if needed. Here function `search(word)` will check if we have given `word` in our trie and `startsWith(prefix)` will check if we have words starting with prefix. 

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.end_node = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word): #None
        root = self.root
        for symbol in word:
            root = root.children.setdefault(symbol, TrieNode())
        root.end_node = 1
        
    def searchHelper(self, word):
        root = self.root
        for symbol in word:
            if symbol in root.children:
                root = root.children[symbol]
            else:
                return -1

        return 1 if root.end_node == 1 else 0  


    def search(self, word): #bool:
        return self.searchHelper(word) == 1

    def startsWith(self, prefix): #bool:
        return self.searchHelper(prefix) >= 0  
```


##### Version 2
Here is a bit different implementation, which potentially can be a bit faster. Sometimes it is useful for each node keep counter of how many times it is here, then functions add and delete will look more similar.

```python
class Trie:
    def __init__(self, words):
        self.root = dict()
        for word in words:
            self.add(word)

    def add(self, word):
        current_dict = self.root
        for letter in word:
            current_dict = current_dict.setdefault(letter, dict())
        current_dict["_end_"] = True

    def __contains__(self, word):
        current_dict = self.root
        for letter in word:
            if letter not in current_dict:
                return False
            current_dict = current_dict[letter]
        return "_end_" in current_dict

    def __delitem__(self, word):
        current_dict = self.root
        nodes = [current_dict]
        for letter in word:
            current_dict = current_dict[letter]
            nodes.append(current_dict)
        del current_dict["_end_"]
```

**Remark:** sometimes it is useful to keep frequency of each word as well, just add one more field to the first version.

#### 2SAT
2SAT problem can be solved in linear time, using strong components. For more details look at https://github.com/cheran-senthil/PyRival/blob/master/pyrival/data_structures/TwoSat.py


#### Convex Hull Trick
Given lines of form $f_i(x) = K_i \cdot x + M_i$, $i = 1,\dots, n$ the goal is to answer queries:

$$\max\limits_{i=1}^n f_i(x) \ \ \ \ (1)$$ 

for different given $x$.

1. `clear_data(KM0)` will return cleaned set of lines: k coefficient will be in increasing order and also for lines with equal `k` only the line with the biggest `m` will be taken. Time complexity is $O(n \log n)$
2. `convex_hull_trick(KM)` will  return 
	`hull_i`: on interval `j`, line `i = hull_i[j]` is >= all other lines;
        `hull_x`: interval `j` and `j + 1` is separated by `x = hull_x[j]`, (`hull_x[j]` is the last `x` in interval `j`)
Time complexity is $O(n)$.
3. `max_query(x)` will return value of equation $(1)$. Complexity is $O(\log n)$.



```python
from bisect import bisect_left

def clear_data(KM0):
    KM0, KM = sorted(KM0 + [(float("inf"), 0)]), []
    for (k1, m1), (k2, m2) in zip(KM0, KM0[1:]):
        if k1 < k2: KM += [(k1, m1)]
    return KM

def convex_hull_trick(KM):
    intersect = lambda i, j: (KM[j][1] - KM[i][1], KM[i][0] - KM[j][0])
    hull_i, hull_x = [0], []

    for i in range(1, len(KM)):
        while True:
            x, y = intersect(i, hull_i[-1])
            if hull_x and x * hull_x[-1][1] <= y * hull_x[-1][0]:
                hull_i.pop()
                hull_x.pop()
            else:
                break
        hull_i += [i]
        hull_x += [(x, y)]
    return hull_i, [x/y for x, y in hull_x]

def max_query(x):
    i = hull_i[bisect_left(hull_x, x)]
    return KM[i][0] * x + KM[i][1]

#### Example
KM0 = [(-2,4), (-1,3), (0,1), (1,0), (0, 0)]
KM = clear_data(KM0)
hull_i, hull_x = convex_hull_trick(KM)
max_query(1.6)
```

**Remark**
I rewrote original algorithm a bit, so now it can work without roundind error: at least `hull_i` have correct order. `hull_x` can have some rounding errors and if we want to avoid floats at all, we need to write simple binary search by hands, where we compare fractions.
