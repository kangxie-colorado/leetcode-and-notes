"""
https://leetcode.com/problems/find-the-derangement-of-an-array/?envType=study-plan&id=dynamic-programming-iii

I could not figure out this alone
but the idea behind it here is pretty classical

think of one elment, element n
it has n-1 choices... [1:n-1] (inclusive)

we can put it to ith, then ith needs be put to another place
1. it can just be put into n-th spot, i.e. a swap of n and 1, then the rest n-2 element face the same problem 
which would be a f(n-2)
2. or it will not be put into n-th spot, while in some sense, it "should" be in n-th spot if not deranged
otherwise, n-1 element vs n-1 positions and each of them should be not at their supposed spot
so that becomes f(n-1)
    ^ this needs some leap of faith anyway.. 

element n can choose any of n-1 spot to do this f(n-2) and f(n-1)
so that means f(n) = (n-1)*(f(n-1)+f(n-2))
    
"""


class Solution:
    def findDerangement(self, n: int) -> int:
        mod = 10**9+7
        dp = [0]*(n+1)
        if n >= 2:
            dp[2] = 1

        for i in range(3, n+1):
            dp[i] = (i-1)*(dp[i-1] + dp[i-2]) % mod

        return dp[n]
    
"""
Runtime: 451 ms, faster than 57.47% of Python3 online submissions for Find the Derangement of An Array.
Memory Usage: 53.8 MB, less than 33.33% of Python3 online submissions for Find the Derangement of An Array.
"""