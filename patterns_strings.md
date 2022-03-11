---
layout: page
title: Patterns Strings
permalink: /patterns/strings
---

Here is a collection of different strings patterns.

#### Prefix function for KMP

Sometimes prefix function can be quite useful for some strings problems. The prefix function for this string is defined as an array $\pi$ of length $n$, where $\pi[i]$ is the length of the longest proper prefix of the substring `s[0...i]` which is also a suffix of this substring. A proper prefix of a string is a prefix that is not equal to the string itself. By definition, $\pi[0] = 0$.

```python
def prefix(s):
    p = [0] * len(s)
    for i in range(1, len(s)):
        k = p[i - 1]
        while k > 0 and s[k] != s[i]:
            k = p[k - 1]
        if s[k] == s[i]:
            k += 1
        p[i] = k
    return p
```

#### Manacher algorighm for palindromes
Not very frequent algorithm, but quite elegant.
It will return lengths of longest palindromes for all $2n-1$ places (there are odd and even places). Time and space complexity is $O(n)$. In my opinion it is quite similar to KMP algorithm.

```python
def manachers(S):
    A = '@#' + '#'.join(S) + '#$'
    Z = [0] * len(A)
    center = right = 0
    for i in range(1, len(A) - 1):
        if i < right:
            Z[i] = min(right - i, Z[2 * center - i])
        while A[i + Z[i] + 1] == A[i - Z[i] - 1]:
            Z[i] += 1
        if i + Z[i] > right:
            center, right = i, i + Z[i]
    return Z[2:-2]
```


#### Suffix array
Let us consider for simplicity example `banana`. Then what we want to construct is list of all suffixes: `banana, anana, nana, ana, na, a` and then sort them in increasing order: we have `a, ana, anana, banana, na, nana`. Actually what we keep is order if indexes: `(5, 3, 1, 0, 4, 2)`, this is called suffix array.

function `suffixArray` given list s returns two pieces of information: `sa` is suffix array itself and `ans` is list of ranks for substrings of lengths `1, 2, 4, ... We can need it for example to compare substrings in O(1) later.

Complexity of construction is $O(n\log^2n)$, but in practice it works quite fast in python, due to built-in sort function. One small optimization is to change break condition `while k < n - 1` to `while max(line) < n - 1` which will break earlier if all ranks are different already.

There is similar way we can do it in $O(n \log n)$ complexity, but in practice it works even slower, because we need to perform bucket sort by hands which will be slow because we need to work with indexes a lot. There is in fact $O(n)$ algorithm constructing suffix trees first, but it is quite painful. 

```python
def ranks(l):
    index = {v: i for i, v in enumerate(sorted(set(l)))}
    return [index[v] for v in l]

def suffixArray(s):
    line = ranks(s)
    n, k, ans, sa = len(s), 1, [line], [0]*len(s)
    while max(line) < n - 1:  #k < n - 1 without optimization
        line = ranks(list(zip_longest(line, islice(line, k, None), fillvalue=-1)))
        ans, k = ans + [line], k << 1
    for i, k in enumerate(ans[-1]): sa[k] = i
    return ans, sa
```

After we constructed suffixArray, we can construct LCP array in $O(n)$ time: this array will consist of biggest common prefixes lengths between pair of adjacent suffixes in suffix array, for our `banana` example we have `a, ana, anana, banana, na, nana`, so answer is `1, 3, 0, 0, 2`. (Use `ans[-1]` from suffixArray code to get `inv_suff`.)

```python
def lcp(Arr, suffixArr, inv_suff):
    n, ans, k = len(arr), [0]*len(arr), 0
    
    for i in range(n):
        if inv_suff[i] == n-1:
            k = 0
            continue

        j = suffixArr[inv_suff[i] + 1]
        while i + k < n and j + k < n and arr[i+k] == arr[j+k]:
            k += 1

        ans[inv_suff[i]] = k
        if k > 0: k -= 1

    return ans
```

##### Implementation 2
Here is `O(len(A) + max(A))` complexity version. Also a bit different version of Kasai, which have only one argument: given `A, SA` it return LCP. Notice however that because we did not construct elements of size 1, 2, 4, ... when we construct suffix array, we can not use tricks to find longest common substring for two substrings and others. Here `LCP` will return two items: `LCP` inself and `rank`, which is the inverse permutation of suffix array. Also it is equal to `sa[-1]`.

```python
def suffixArray(A):
    n = len(A)
    buckets = [0] * (max(A) + 2)
    for a in A:
        buckets[a + 1] += 1
    for b in range(1, len(buckets)):
        buckets[b] += buckets[b - 1]
    isL = [1] * n
    for i in reversed(range(n - 1)):
        isL[i] = +(A[i] > A[i + 1]) if A[i] != A[i + 1] else isL[i + 1]
 
    def induced_sort(LMS):
        SA = [-1] * (n)
        SA.append(n)
        endpoint = buckets[1:]
        for j in reversed(LMS):
            endpoint[A[j]] -= 1
            SA[endpoint[A[j]]] = j
        startpoint = buckets[:-1]
        for i in range(-1, n):
            j = SA[i] - 1
            if j >= 0 and isL[j]:
                SA[startpoint[A[j]]] = j
                startpoint[A[j]] += 1
        SA.pop()
        endpoint = buckets[1:]
        for i in reversed(range(n)):
            j = SA[i] - 1
            if j >= 0 and not isL[j]:
                endpoint[A[j]] -= 1
                SA[endpoint[A[j]]] = j
        return SA
 
    isLMS = [+(i and isL[i - 1] and not isL[i]) for i in range(n)]
    isLMS.append(1)
    LMS = [i for i in range(n) if isLMS[i]]
    if len(LMS) > 1:
        SA = induced_sort(LMS)
        LMS2 = [i for i in SA if isLMS[i]]
        prev = -1
        j = 0
        for i in LMS2:
            i1 = prev
            i2 = i
            while prev >= 0 and A[i1] == A[i2]:
                i1 += 1
                i2 += 1
                if isLMS[i1] or isLMS[i2]:
                    j -= isLMS[i1] and isLMS[i2]
                    break
            j += 1
            prev = i
            SA[i] = j
        LMS = [LMS[i] for i in suffixArray([SA[i] for i in LMS])]
    return induced_sort(LMS)
 
def lcp(A, SA):
    n = len(A)
    rank = [0] * n
    for i in range(n):
        rank[SA[i]] = i
    LCP = [0] * (n - 1)
    k = 0
    for i in range(n):
        SAind = rank[i]
        if SAind == n - 1:
            continue
        j = SA[SAind + 1]
        while i + k < n and A[i + k] == A[j + k]:
            k += 1
        LCP[SAind] = k
        k -= k > 0
    return LCP, rank
```