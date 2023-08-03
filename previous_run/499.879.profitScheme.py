""""
https://leetcode.com/problems/profitable-schemes/?envType=study-plan&id=dynamic-programming-iii

not so easy this one?

f(n,idx, req):
    represents with n members, at idx crime, how many combinations could match req profit 
    it will be 
        taking idx
            f(n-group[idx], idx+1, req-profit[idx])
        not-taking idx
            f(n, idx+1, req)
    
    base:
        req<=0: 
            return leftNum * (leftNum-1) // 2

        n<=0: 
            # when req>0, no more people.. this will not be possible
            return 0

        idx==n:
            and req>0.. not possible either
            return 0
        

"""


from functools import cache
from typing import List


class Solution:
    def profitableSchemes(self, n: int, minProfit: int, group: List[int], profit: List[int]) -> int:
        l = len(group)
        mod = 10**9+7

        @cache
        def f(leftGang, idx, req):
            if idx==l or leftGang<=0:
                return 0

            # not doing this crime
            res = f(leftGang, idx+1, req) 
            # doing this crime
            if leftGang>=group[idx]:
                if profit[idx] >= req:
                    res += 1 + f(leftGang-group[idx], idx+1, req-profit[idx])
                else:
                    res += f(leftGang-group[idx], idx+1, req-profit[idx]) 
            # print(leftGang, idx, req, res)
            return res % mod
        
        ways = f(n, 0, minProfit)
        return ways if minProfit else ways+1

""""
okay.. the logic was a little more complicated than I outlined in the top..
but still failed
64
0
[80, 40]
[88, 88]

why it should be 2??
oh.. fuck.. if it is 0, then not doing anything is also a zero

hmm.. still TLE....

"""


class Solution:
    def profitableSchemes(self, n: int, minProfit: int, group: List[int], profit: List[int]) -> int:
        l = len(group)
        mod = 10**9+7

        @cache
        def f(leftGang, idx, req):
            if idx == l or leftGang <= 0:
                return 0

            # not doing this crime
            res = f(leftGang, idx+1, req) % mod
            # doing this crime
            if leftGang >= group[idx]:
                if profit[idx] >= req:
                    res += 1
                res += f(leftGang-group[idx], idx+1, req-profit[idx]) % mod
            # print(leftGang, idx, req, res)
            return res % mod

        ways = f(n, 0, minProfit)
        return ways if minProfit else ways+1

"""
okay.. later turn this into bottom up

later.. not today.. 
go packing

hmm.. maybe another sub problem
when req<=0, then I just see how many combination to meet the leftGang?
"""


class Solution:
    def profitableSchemes(self, n: int, minProfit: int, group: List[int], profit: List[int]) -> int:
        l = len(group)
        mod = 10**9+7

        @cache
        def ways(leftGang, idx, req):
            if idx == l or leftGang <= 0:
                return 0

            # not doing this crime
            res = ways(leftGang, idx+1, req) % mod
            # doing this crime
            if leftGang >= group[idx]:
                if profit[idx] >= req:
                    res += 1 + groupWays(leftGang-group[idx], idx+1)
                else:
                    res += ways(leftGang-group[idx], idx+1, req-profit[idx]) % mod
            # print(leftGang, idx, req, res)
            return res % mod

        # when request is already 0.. 
        # could take this short cut
        @cache
        def groupWays(leftGang, idx):
            if idx == l or leftGang <= 0:
                return 0
            
            res = groupWays(leftGang, idx+1)
            if leftGang >= group[idx]:
                res += 1+groupWays(leftGang-group[idx], idx+1)
            return res

        ways = ways(n, 0, minProfit)
        return ways if minProfit else ways+1

"""
Runtime: 3658 ms, faster than 23.12% of Python3 online submissions for Profitable Schemes.
Memory Usage: 172.6 MB, less than 13.87% of Python3 online submissions for Profitable Schemes.

okay.. study further but later..
"""
            
if __name__ == '__main__':
    s = Solution()
    print(s.profitableSchemes(n=5, minProfit=3, group=[2, 2], profit=[2, 3]))
    print(s.profitableSchemes(n=10, minProfit=5,
          group=[2, 3, 5], profit=[6, 7, 8]))
    print(s.profitableSchemes(1,1,[2,2,2,2,2],[1,2,1,1,0]))