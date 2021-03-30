### Problem statement:

You are given a 2D array of integers envelopes where \texttt{envelopes[i] = [wi, hi]} represents the width and the height of an envelope.

One envelope can fit into another if and only if both the width and height of one envelope is greater than the width and height of the other envelope.

Return the maximum number of envelopes can you Russian doll (i.e., put one inside the other).

### Solution:

```
class Solution:
    def maxEnvelopes(self, envelopes):
        nums = sorted(envelopes, key = lambda x: [x[0], -x[1]])    
        dp = [10**10] * (len(nums) + 1)
        for elem in nums: dp[bisect_left(dp, elem[1])] = elem[1]  
        return dp.index(10**10)
```