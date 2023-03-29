"""
https://leetcode.com/problems/count-ways-to-distribute-candies/?envType=study-plan&id=dynamic-programming-iii

sounds like a straight forwar dp
I can just write the top down

f(n,k): at n-th candy and k remain bags
    it can go into k bags so k + f(n-1,k)

    this seems like it could take care of the order as well

nah.. this is dead wrong.. 
cannot be that simple anyway..

first of all.. at least one candy in one bag
so that means -- we need k candies from n to cover this at least 
    this means we have C[n,k] choices... 
    n=3,k=2.. that means.. we have 3*2/2=3 choices to fill the bad with one candy first 

    then the left candy, which is 1.. can actually be put in one bag.. so what?
    (1) (2) -> (1,3) (2) or (1) (2,3)
    (1) (3) -> (1,2) (3) or (1) (2,3)
    (2) (3) -> (1,2) (3) or (2) (1,3)
hmm... not so right 

check the hints

Try to define a recursive approach. For the ith candies, there will be one of the two following cases:

1. If the i - 1 previous candies are already distributed into k bags for the ith candy, you can have k * dp[n - 1][k] ways to distribute the ith candy. 
    We need then to solve the state of (n - 1, k).
    okay.. make sense here.. that means kth candy can go anywhere
2. If the i - 1 previous candies are already distributed into k - 1 bags for the ith candy, you can have dp[n - 1][k - 1] ways to distribute the ith candy. 
    We need then to solve the state of (n - 1, k - 1).
    that means it need to fill the k-th bags, so left us with n-1 candy , to fill k-1 bags.. 
3. This approach will be too slow and will traverse some states more than once. We should use memoization to make the algorithm efficient.
    of course..

but why above two sub-problems can be right? yeah.. they recurse..

think 
    if k==n, then only one way
    if n==k+1, then only k way right?
        hmm.. not right
        n=3,k=2 that is 3.. 

        for n at 3, there are two subproblems
            each bag has 1, thus this gives 2 
            one bag has 0 and the other has 2, this only give 1 possibility.. must fill the empty one
            this goes with the 2nd case... we must fill this candy to k-th bag.. but for n-1 candy, k-1 bag, there can be dp[n-1][k-1] ways 
            so somehow it translates to possibilities of i-th candy as well

"""


from functools import cache


class Solution:
    def waysToDistribute(self, n: int, k: int) -> int:
        mod = 10**9 + 7

        @cache
        def f(n,k):
            if n==k:
                return 1
            
            if k==0:
                return 0
            
            res = f(n-1,k)*k + f(n-1,k-1)
            return res%mod

        return f(n,k)

"""
105 / 105 test cases passed, but took too much memory.
okay.. bottom up then
"""    


class Solution:
    def waysToDistribute(self, n: int, k: int) -> int:
        mod = 10**9 + 7

        dp = [[0]*(k+1) for _ in range(n+1)]
        for i in range(1,n+1):
            for j in range(1,k+1):
                if i==j:
                    dp[i][j] = 1
                    continue
                dp[i][j] = (dp[i-1][j]*j + dp[i-1][j-1])%mod
        return dp[n][k]

"""
Runtime: 5805 ms, faster than 17.31% of Python3 online submissions for Count Ways to Distribute Candies.
Memory Usage: 36 MB, less than 50.00% of Python3 online submissions for Count Ways to Distribute Candies.
"""



if __name__ == '__main__':
    s = Solution()
    print(s.waysToDistribute(3,2))
    print(s.waysToDistribute(4,2))