"""
https://leetcode.com/problems/paint-house/

hmm... cost and house to form a 2D DP array????

or sub-problems 

f(0) = min(
    cost[1][0] + f(1, not [0])
    cost[1][1] + f(1, not [1])
    cost[1][2] + f(1, not [2])

    on last houst, take the minimum of available choices 
 )

"""


from functools import cache
from typing import List


class Solution:
    def minCost(self, costs: List[List[int]]) -> int:

        @cache
        def helper(idx, lastColor):
            if idx == len(costs):
                return 0

            res = float('inf')
            for choice, cost in enumerate(costs[idx]):
                if choice != lastColor:
                    res = min(res, cost + helper(idx+1, choice))

            return res

        return helper(0, -1)

"""
Runtime: 134 ms, faster than 34.07% of Python3 online submissions for Paint House.
Memory Usage: 14.3 MB, less than 18.83% of Python3 online submissions for Paint House.

there is such a DP solution 

class Solution(object):
    def minCost(self, costs):
        red, blue, green = 0, 0, 0
        for cr, cb, cg in costs:
            red, blue, green = min(blue, green) + cr, min(red, green) + cb, min(red, blue) + cg
        return min(red, blue, green)

pretty impressive..
but turns out my code can solve the hard paint house II with no change

https://leetcode.com/problems/paint-house-ii/submissions/
Runtime: 270 ms, faster than 47.62% of Python3 online submissions for Paint House II.
Memory Usage: 15.3 MB, less than 12.17% of Python3 online submissions for Paint House II.

there are other solutions requiring less memory or iterative
I am too spent today.. check that later if I came across it again
"""