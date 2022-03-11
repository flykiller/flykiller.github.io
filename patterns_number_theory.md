---
layout: page
title: Patterns Number Theory and Algebra
permalink: /patterns/number theory
---

Here is a collection of different number theory and algebra patterns.

#### Factorials
Sometimes it is useful to precalculate all factorials and inverse factorials given prime modulo: then we can evaluate numbers of combinations in `O(1)`. Time to precalculate is `O(M)`.

```python
MOD, M = 10**9 + 7, 10**5
F = [1]*(M+1)
for i in range(1, M+1):
    F[i] = (F[i-1] * i) % MOD

I = [1]*M + [pow(F[M], MOD - 2, MOD)]
for i in range(M-1, 0, -1):
    I[i] = I[i+1]*(i+1) % MOD
```


#### Chinese reminder theorem
1. `gcd(x, y)` returns common divisor of `x` and `y`.
2. `chinese_remainder(a, p)` is special case of chinese remindrer theorem, where all `p` are primes: returns `x` s.t. `x = a[i] (mod p[i])` where `p[i]` is prime for all `i`.
3. `extended_gcd(a, b)` will return `gcd(a, b), s, r` s.t. `a * s + b * r == gcd(a, b)`
4. `composite_crt` returns `x` s.t. `x = b[i] (mod m[i])` for all `i`

```python
import operator as op
from functools import reduce

def gcd(x, y):
    while y:
        x, y = y, x % y
    return x

def chinese_remainder(a, p):
    prod = reduce(op.mul, p, 1)
    x = [prod // pi for pi in p]
    return sum(a[i] * pow(x[i], p[i] - 2, p[i]) * x[i] for i in range(len(a))) % prod

def extended_gcd(a, b):
    s, old_s = 0, 1
    r, old_r = b, a
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
    return old_r, old_s, (old_r - old_s * a) // b if b else 0

def composite_crt(b, m):
    x, m_prod = 0, 1
    for bi, mi in zip(b, m):
        g, s, _ = extended_gcd(m_prod, mi)
        if ((bi - x) % mi) % g:
            return None
        x += m_prod * (s * ((bi - x) % mi) // g)
        m_prod = (m_prod * mi) // gcd(m_prod, mi)
    return x % m_prod
```

#### Discrete Logarithm

To solve equation (discrete logarithm) $a^x \equiv b (m)$ if $(a, m) = 1$ we can use idea of meet-in-the-middle with complexity $O(\sqrt{m})$, this is called Shanks theorem.

Returns smallest `x > 0` s.t. `pow(a, x, mod) == b` or `None` if no such `x` exists.
Note: works even if a and mod are not coprime.

```python
def discrete_log(a, b, mod):
    n = int(mod**0.5) + 1

    # tiny_step[x] = maximum j <= n s.t. b * a^j % mod = x
    tiny_step, e = {}, 1
    for j in range(1, n + 1):
        e = e * a % mod
        if e == b:
            return j
        tiny_step[b * e % mod] = j

    # find (i, j) s.t. a^(n * i) % mod = b * a^j % mod
    factor = e
    for i in range(2, n + 2):
        e = e * factor % mod
        if e in tiny_step:
            j = tiny_step[e]
            return n * i - j if pow(a, n * i - j, mod) == b else None
```

#### LCM and GCD
LCM and GCD are already defined in python and I think it works pretty fast. However here is implementation by hands. Also see Chinese reminder theorem section for extended gcd.
   
```python
def gcd(x, y):
    while y:
        x, y = y, x % y
    return x

gcdm = lambda *args: reduce(gcd, args, 0)

lcm = lambda a, b: a * b // gcd(a, b)

lcmm = lambda *args: reduce(lcm, args, 1)
```

#### Numbers factorization
##### Small numbers version
If we want to have fast factorization of small numbers, we can precalculate all smallest prime factors. Time to precalculate is `O(M log M)` and then time to factorize is `O(log M)`.
```python
arr = [0]*(M+1)
for i in range(2, M+1):
    for j in range(i, M+1, i):
        if arr[j] == 0: arr[j] = i

def factorize(k):
    primes = []
    while arr[k] != 0:
        primes += [arr[k]]
        k //= arr[k]
    return primes
```


##### Big numbers version
You should use this if you need to factorize quite big number, using rho Pollard algorithm. Time complexity can be estimated as `O(n^(1/4))`

```python
def pollard_rho(n):
    """returns a random factor of n"""
    if n & 1 == 0:
        return 2
    if n % 3 == 0:
        return 3

    s = ((n - 1) & (1 - n)).bit_length() - 1
    d = n >> s
    for a in [2, 325, 9375, 28178, 450775, 9780504, 1795265022]:
        p = pow(a, d, n)
        if p == 1 or p == n - 1 or a % n == 0:
            continue
        for _ in range(s):
            prev = p
            p = (p * p) % n
            if p == 1:
                return gcd(prev - 1, n)
            if p == n - 1:
                break
        else:
            for i in range(2, n):
                x, y = i, (i * i + 1) % n
                f = gcd(abs(x - y), n)
                while f == 1:
                    x, y = (x * x + 1) % n, (y * y + 1) % n
                    y = (y * y + 1) % n
                    f = gcd(abs(x - y), n)
                if f != n:
                    return f
    return n

@lru_cache
def prime_factors(n):
    """returns a Counter of the prime factorization of n"""
    if n <= 1:
        return Counter()
    f = pollard_rho(n)
    return Counter([n]) if f == n else prime_factors(f) + prime_factors(n // f)

def distinct_factors(n):
    """returns a list of all distinct factors of n"""
    factors = [1]
    for p, exp in prime_factors(n).items():
        factors += [p**i * factor for factor in factors for i in range(1, exp + 1)]
    return factors

def all_factors(n):
    """returns a sorted list of all distinct factors of n"""
    small, large = [], []
    for i in range(1, int(n**0.5) + 1, 2 if n & 1 else 1):
        if not n % i:
            small.append(i)
            large.append(n // i)
    if small[-1] == large[-1]:
        large.pop()
    large.reverse()
    small.extend(large)
    return small
```

#### Fast Fourier Transform
We can use it to multiply two polynomials (get convoluiton of them) in `O(n log n)` time. I think it will work fine if `n` is not more than around `100000`, if it is bigger, we will have rounding error.
There is also `np.convolve` function, but it works 10 times slower, may be it is not using FFT.

```python
import cmath

def fft(a, inv=False):
    n = len(a)
    w = [cmath.rect(1, (-2 if inv else 2) * cmath.pi * i / n) for i in range(n >> 1)]
    rev = [0] * n
    for i in range(n):
        rev[i] = rev[i >> 1] >> 1
        if i & 1:
            rev[i] |= n >> 1
        if i < rev[i]:
            a[i], a[rev[i]] = a[rev[i]], a[i]

    step = 2
    while step <= n:
        half, diff = step >> 1, n // step
        for i in range(0, n, step):
            pw = 0
            for j in range(i, i + half):
                v = a[j + half] * w[pw]
                a[j + half] = a[j] - v
                a[j] += v
                pw += diff
        step <<= 1

    if inv:
        for i in range(n):
            a[i] /= n


def fft_conv(a, b):
    s = len(a) + len(b) - 1
    n = 1 << s.bit_length()
    a.extend([0.0] * (n - len(a)))
    b.extend([0.0] * (n - len(b)))

    fft(a), fft(b)
    for i in range(n):
        a[i] *= b[i]
    fft(a, True)

    a = [a[i].real for i in range(s)]
    return a
```

#### Subset manipulations
First problem is given array `arr` find sums of all subsets of given list `arr` and its length `n`.
```python
def subset_sums(arr, n):
    mask_sum = [0]*(1<<n)
    for mask, i in product(range(1<<n), range(n)):
        if (1 << i) & mask:
            mask_sum[mask] += arr[i]
    return mask_sum
```

Notation:

1. set `s` and mask `s` are used interchangeably meaning the same thing.
2. `a\b` would mean set subtraction, i.e subtracting set `b` from set `a`.
3. `|s|` refers to the cardinality, i.e the size of the set `s`.
4. $\sum\limits_{s' \subseteq s} f(s')$ refers to summing function `f` over all possible subsets (aka submasks) `s'` of `s`.

Aim: Given functions `f` and `g` both from $[0, 2^n)$ to integers. Can be represented as arrays `f[]` and `g[]` respectively in code. We want to compute the following transformations fast:

##### Zeta Transform
Also called SOS DP/Yate's DP: $z(f(s)) = \sum\limits_{s' \subseteq s} f(s')$ for all $s \in [0,2^n)$ in $O(n\cdot 2^n)$.
Note, that this is an extension of sum of subsets problem, where we have `F[2^i] = arr[i]`.

Example: `F = [1, 2, 3, 4, 5, 6, 7, 8]`. Then `Z = zeta(3, F) = [1, 3, 4, 10, 6, 14, 16, 36]`, because:
1. For bitmask `000`, we have only one subset `000`, so `Z[0] = F[0]`.
2. For bitmask `001`, we have `Z[1] = F[0] + F[1] = 3`.
3. For bitmask `010`, we have `Z[2] = F[0] + F[2] = 4`.
4. For bitmask `011`, we have `Z[3] = F[0] + F[1] + F[2] + F[3] = 10`.
5. For bitmask `100`, we have `Z[4] = F[0] + F[4] = 6`.
6. For bitmask `101`, we have `Z[5] = F[0] + F[1] + F[4] + F[5] = 14`.
7. For bitmask `110`, we have `Z[6] = F[0] + F[2] + F[4] + F[6] = 16`.
8. For bitmask `111`, we have `Z[7] = F[0] + F[1] + F[2] + F[3] + F[4] + F[5] + F[6] + F[7] = 36`.

```python
def zeta(n, F):
    Z = F[:]
    for b, i in product(range(n), range(1<<n)):
        if i & 1 << b:
            Z[i] += Z[i ^ (1 << b)]
    return Z
```

##### Mobius Transform
i.e. inclusion exclusion sum over subset: 
$\mu(f(s)) = \sum\limits_{s' \subseteq s}(-1)^{|s\backslash s'|}f(s')$,
for all $s\in [0, 2^n)$ in $O(n\cdot 2^n)$. 
Here the term $(-1)^{|s\backslash s'|}$ just looks intimidating but simply means whether we should add the term or subtract the term in Inclusion-Exclusion Logic.

Example: `F = [1, 3, 6, 14, 17, 23, 30, 63]`. Then `Z = mu(3, F) = [1, 2, 5, 6, 16, 4, 8, 21]`, because:
1. For bitmask `000`, we have only one subset `000`, so `Z[0] = F[0]`.
2. For bitmask `001`, we have `Z[1] = F[1] - F[0] = 2`.
3. For bitmask `010`, we have `Z[2] = F[2] - F[0] = 5`.
4. For bitmask `011`, we have `Z[3] = F[3] - F[1] - F[2] + F[0] = 6`.
5. For bitmask `100`, we have `Z[4] = F[4] - F[0] = 16`.
6. For bitmask `101`, we have `Z[5] = F[5] - F[1] - F[4] + F[0] = 4`.
7. For bitmask `110`, we have `Z[6] = F[6] - F[2] - F[4] + F[0] = 8`.
8. For bitmask `111`, we have `Z[7] = F[7] - F[3] - F[5] - F[6] + F[1] + F[2] + F[4] - F[0] = 21`.

```python
def mu(n, F):
    M = F[:]
    for b, i in product(range(n), range(1<<n)):
        if i & 1 << b:
            M[i] -= M[i ^ (1 << b)]
    return M
```


##### Subset Sum Convolution
Also called Fast Subset Transform: $f\circ g(s) = \sum\limits_{s'\subseteq s} f(s')g(s\backslash s')$ for all $s \in [0,2^n)$ in $O(n^2\cdot 2^n)$. In simpler words, take all possible ways to partition set s into two disjoint partitions and sum over product of f on one partition and g on the complement of that partition.

Example: `F = [1, 2, 3, 4, 5, 6, 7, 8]` and `G = [9, 10, 11, 12, 13, 14, 15, 16]`. Then `C = F` $\circ$ `G = [9, 28, 38, 100, 58, 144, 172, 408]`, because:

1. For bitmask `000`, we have `C[0] = F[0] * G[0] = 1 * 9 = 9`.
2. For bitmask `001`, we have `C[1] = F[0] * G[1] + F[1] * G[0] = 28`.
3. For bitmask `010`, we have `C[2] = F[0] * G[2] + F[2] * G[0] = 38`.
4. For bitmask `011`, we have `C[3] = F[0] * G[3] + F[1] * G[2] + F[2] * G[1] + F[3] * G[0] = 100`.
5. For bitmask `100`, we have `C[4] = F[0] * G[4] + F[4] * G[0] = 58`.
6. For bitmask `101`, we have `C[5] = F[0] * G[5] + F[1] * G[4] + F[4] * G[1] + F[5] * G[0] = 144`.
7. For bitmask `110`, we have `C[6] = F[0] * G[6] + F[2] * G[4] + F[4] * G[2] + F[6] * G[0] = 172`.
8. For bitmask `111`, we have `C[7] = F[0] * G[7] + F[1] * G[6] + F[2] * G[5] + F[3] * G[4] + F[4] * G[3] + F[5] * G[2] + F[6] * G[1] + F[7] * G[0] = 408`.

```python
def conv(n, F, G):
    fhat = [[0]*(1<<n) for _ in range(n+1)]
    ghat = [[0]*(1<<n) for _ in range(n+1)]
    h = [[0]*(1<<n) for _ in range(n+1)]

    for m in range(1<<n):
        fhat[bin(m).count("1")][m] = F[m]
        ghat[bin(m).count("1")][m] = G[m]

    for i in range(n + 1):
        for j in range(n):
            for m in range(1<<n):
                if m & (1 << j) != 0:
                    fhat[i][m] += fhat[i][m ^ (1<<j)]
                    ghat[i][m] += ghat[i][m ^ (1<<j)]

    for m in range(1<<n):
        for i in range(n + 1):
            for j in range(i + 1):
                h[i][m] += fhat[j][m] * ghat[i-j][m]

    for i in range(n + 1):
        for j in range(n):
            for m in range(1<<n):
                if m & (1<<j) != 0:
                    h[i][m] -= h[i][m ^ (1<<j)]

    return [h[bin(m).count("1")][m] for m in range(1<<n)]
```

For proofs and more details look at https://codeforces.com/blog/entry/72488

See also https://cp-algorithms.com/combinatorics/inclusion-exclusion.html for Mobius Transform

Here is an implementation of subset sum convolution. There is also implementation here https://github.com/cheran-senthil/PyRival/blob/master/pyrival/algebra/fst.py, but I am not sure how to use it.

#### Number Theoretic Transform
This is used for fast polynomials product with complexity `O(n log n)` given module `MOD`. I modified this version for python, it works may be 5% slower than original one from Pyrival site, but it is more clean and I think it works for more prime MOD without magic constants (it still need to be equal `2^x*T + 1` and it will work only for powers `<= 2^x`). However be careful for other `MOD`, you need to choose `ROOT` as well, so it is primitive root (**check**).

```python
MOD, ROOT = 998244353, 3
 
def ntt(a, inv=0):
    n = len(a)
    w = [1] * (n >> 1)
    w[1] = pow(ROOT, (MOD - 1)//n * (inv*(MOD-3) + 1), MOD)
 
    for i in range(2, n >> 1): 
        w[i] = (w[i - 1] * w[1]) % MOD
 
    rev = [0] * n
    for i in range(n):
        rev[i] = rev[i >> 1] >> 1
        if i & 1:
            rev[i] |= n >> 1
        if i < rev[i]:
            a[i], a[rev[i]] = a[rev[i]], a[i]

    log_n = (n+1).bit_length()
    for i in range(1, log_n):
        half, diff = 1<<(i-1), log_n - i - 1
        for j in range(0, n, 1<<i):
            for k in range(j, j + half):
                v = (w[(k-j)<<diff] * a[k + half]) % MOD
                a[k + half] = a[k] - v
                a[k] += v
 
    if not inv: return
    inv_n = pow(n, MOD - 2, MOD)
    for i in range(n):
        a[i] = (a[i] * inv_n) % MOD
 
 
def ntt_conv(a, b):
    l1, l2 = len(a), len(b)
    s = l1 + l2 - 1
    n = 1 << s.bit_length()
 
    a += [0] * (n - l1)
    b += [0] * (n - l2)
 
    ntt(a)
    ntt(b)
 
    for i in range(n):
        a[i] = (a[i] * b[i]) % MOD
 
    ntt(a, True)
    del a[s:]
```

#### Deterministic Miller-Rabin Primality Test
It helps us to test quickly (potentially in `O(log^4 n)` if number is prime or not. However I am not sure about given code, what are the limits of it, need to be checked. Also to make it work, generalized Riemann hypothesis needs to be true.

```python
def is_prime(n):
    """returns True if n is prime else False"""
    if n < 5 or n & 1 == 0 or n % 3 == 0:
        return 2 <= n <= 3
    s = ((n - 1) & (1 - n)).bit_length() - 1
    d = n >> s
    for a in [2, 325, 9375, 28178, 450775, 9780504, 1795265022]:
        p = pow(a, d, n)
        if p == 1 or p == n - 1 or a % n == 0:
            continue
        for _ in range(s):
            p = (p * p) % n
            if p == n - 1:
                break
        else:
            return False
    return True
```

#### Modular root
The Tonelli-Shanks algorithm is used in modular arithmetic to solve for $r$ in a congruence of the form $r^2 \equiv n (\mod p)$, where $p$ is a prime: that is, to find a square root of $n$ modulo $p$.

Complexity is something between $O(\log p)$ and $O(\log^2 p)$, but in practice it works quite fast. 

```python
def mod_sqrt(a, p):
    """returns x s.t. x**2 == a (mod p)"""
    a %= p
    if a == 0:
        return 0
    assert pow(a, (p - 1) // 2, p) == 1
    if p & 3 == 3:
        return pow(a, (p + 1) // 4, p)

    r = ((p - 1) & (1 - p)).bit_length() - 1
    s, n = p >> r, 2
    while pow(n, (p - 1) // 2, p) != p - 1:
        n += 1

    x, b, g = pow(a, (s + 1) // 2, p), pow(a, s, p), pow(n, s, p)
    while True:
        t = b
        for m in range(r):
            if t == 1:
                break
            t = (t * t) % p
        if m == 0:
            return x

        gs = pow(g, 1 << (r - m - 1), p)
        g, x = (gs * gs) % p, (x * gs) % p
        b, r = (b * g) % p, m
```

#### Generalized Modular Inverse
Here we want to find $a^{-1} (\mod m)$, where $(a, m) = 1$. For this we just use extended_gcd from `gcd and lcm` part.

```python
def modinv(a, m):
    g, x, _ = extended_gcd(a % m, m)
    return x % m if g == 1 else None
```

#### Euler phi function
Returns `phi(x)` for all `x <= n`, works in `O(n log n)` I think.

```python
def phi(n):
    sieve = [i if i & 1 else i // 2 for i in range(n + 1)]
    for i in range(3, n + 1, 2):
        if sieve[i] == i:
            for j in range(i, n + 1, i):
                sieve[j] = (sieve[j] // i) * (i - 1)

    return sieve
```

#### Primitive root

1. `ilog` returns the smallest `a, b` s.t. `a**b = n` for integer `a, b`
2. `primitive_root` returns primitive root of `p`

In modular arithmetic, a number `g` is called a primitive root modulo `n` if every number coprime to `n` is congruent to a power of `g` modulo `n`. Mathematically, `g` is a primitive root modulo n if and only if for any integer a such that `gcd(a, n) = 1`, there exists an integer `k` such that:
$g^k\equiv a(\mod n)$.
`k` is then called the index or discrete logarithm of a to the base `g` modulo `n`. `g` is also called the generator of the multiplicative group of integers modulo `n`.

In particular, for the case where `n` is a prime, the powers of primitive root runs through all numbers from `1` to `n-1`.

```python
def ilog(n):
    a = n.bit_length()
    for b in range(a, 0, -1):
        lo, hi = 1, 1 << (a // b + 1)
        while lo < hi:
            mi = (lo + hi) // 2
            a_b = mi**b
            if a_b == n:
                return mi, b
            if a_b > n:
                hi = mi
            else:
                lo = mi + 1


def primitive_root(p):
    factors = prime_factors(p - 1)

    for i in range(2, p + 1):
        ok = True
        for j in factors:
            ok &= pow(i, (p - 1) // j, p) != 1
        if ok:
            return i

    return None
```

#### Sieve of Eratosthenes
Here is an optimized version of siever of Erathosthenes, which work for `n = 10^7` around only `2` seconds, which is quite fast for python.

```python
def prime_sieve(n):
    """returns a sieve of primes >= 5 and < n"""
    flag = n % 6 == 2
    sieve = bytearray((n // 3 + flag >> 3) + 1)
    for i in range(1, int(n**0.5) // 3 + 1):
        if not (sieve[i >> 3] >> (i & 7)) & 1:
            k = (3 * i + 1) | 1
            for j in range(k * k // 3, n // 3 + flag, 2 * k):
                sieve[j >> 3] |= 1 << (j & 7)
            for j in range(k * (k - 2 * (i & 1) + 4) // 3, n // 3 + flag, 2 * k):
                sieve[j >> 3] |= 1 << (j & 7)
    return sieve


def prime_list(n):
    """returns a list of primes <= n"""
    res = []
    if n > 1:
        res.append(2)
    if n > 2:
        res.append(3)
    if n > 4:
        sieve = prime_sieve(n + 1)
        res.extend(3 * i + 1 | 1 for i in range(1, (n + 1) // 3 + (n % 6 == 1)) if not (sieve[i >> 3] >> (i & 7)) & 1)
    return res
```
