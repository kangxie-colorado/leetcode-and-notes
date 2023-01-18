"""
https://leetcode.com/problems/maximum-length-of-pair-chain/?envType=study-plan&id=dynamic-programming-ii


think this is just a variation of LIS problem
but we save the right-point in the LIS.. and compare with the left

when there is overlapp.. I still take the smaller right edge

because the isn't required to follow order..
so I'd better sort, by left? or by right? I think by right
"""


import bisect
from typing import List


class Solution:
    def findLongestChain(self, pairs: List[List[int]]) -> int:
        # this is just LIS with a little more twist
        pairs.sort(key=lambda x: x[1])
        lis = [pairs[0][1]]

        for s, e in pairs[1:]:
            if s > lis[-1]:
                lis.append(e)
            else:
                idx = bisect.bisect_left(lis, s)
                lis[idx] = min(lis[idx], e)

        return len(lis)

"""
Runtime: 218 ms, faster than 84.54% of Python3 online submissions for Maximum Length of Pair Chain.
Memory Usage: 14.4 MB, less than 36.56% of Python3 online submissions for Maximum Length of Pair Chain.

ah... I thought it might not pass
but turns out there is an even simpler solution 
"""


class Solution:
    def findLongestChain(self, pairs):
        pairs.sort(key=lambda x: x[1])
        ans = 0
        cur = float('-inf')
        for head, tail in pairs:
            if head > cur:
                cur = tail
                ans += 1
        return ans

"""
Runtime: 217 ms, faster than 85.12% of Python3 online submissions for Maximum Length of Pair Chain.
Memory Usage: 14.3 MB, less than 79.48% of Python3 online submissions for Maximum Length of Pair Chain.

so it kind of focuses on only tail... 
and this below also passes
    - basically, you sort the pairs by end and greedily taking smallest end 
    - ... so what the hell

"""


class Solution:
    def findLongestChain(self, pairs: List[List[int]]) -> int:
        # this is just LIS with a little more twist
        pairs.sort(key=lambda x: x[1])
        lis = [pairs[0][1]]

        for s, e in pairs[1:]:
            if s > lis[-1]:
                lis.append(e)

        return len(lis)
