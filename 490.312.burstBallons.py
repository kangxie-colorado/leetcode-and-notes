"""
https://leetcode.com/problems/burst-balloons/

okay.. I knew this is a interval dp type problem
this problem is to fix a point in an interval [i,j] - i<=k<=j

then k will be last ballon to shoot for
then this problem can be divided into 
max{  dp[i,k-1]+dp[k+1,j]+nums[k]*(nums[i-1]*nums[j+1]), for k in [i,j]}

worthy noting is how to first find the interval
fix i,j? that probably works better in recursive form
so maybe fix length and start, that could work in iterative form

so I watched/listened to the video in iterative form
let me try solving this in recursive form

"""


from functools import cache
from typing import List


class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        n = len(nums)
        nums = [1] + nums + [1]

        @cache
        def f(i,j):
            if i==j:
                return nums[i-1]*nums[i]*nums[j+1]
            
            if i>j:
                return 0
            
            res = 0
            for k in range(i,j+1):
                res = max(res, f(i,k-1) + f(k+1,j) + nums[k]*nums[i-1]*nums[j+1])
            
            return res
        
        return f(1,n)

"""
Runtime: 11124 ms, faster than 22.21% of Python3 online submissions for Burst Balloons.
Memory Usage: 30.8 MB, less than 25.35% of Python3 online submissions for Burst Balloons.

the base can be slightly simplified
"""


class Solution:
    def maxCoins(self, nums: List[int]) -> int:
        n = len(nums)
        nums = [1] + nums + [1]

        @cache
        def f(i, j):
            if i > j:
                return 0

            res = 0
            for k in range(i, j+1):
                res = max(res, f(i, k-1) + f(k+1, j) +
                          nums[k]*nums[i-1]*nums[j+1])

            return res

        return f(1, n)

if __name__ == '__main__':
    s = Solution()
    print(s.maxCoins(nums = [3,1,5,8]))
    print(s.maxCoins(nums = [1,5]))