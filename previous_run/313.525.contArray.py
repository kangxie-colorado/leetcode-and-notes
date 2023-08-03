"""
https://leetcode.com/problems/contiguous-array/

think to start from left and right - two pointers

"""


from collections import defaultdict
from typing import Counter, List


class Solution:
    def findMaxLength(self, nums: List[int]) -> int:
        C = Counter(nums)
        l, r = 0, len(nums)-1

        while True:
            if C[1] == C[0]:
                return r-0+1

            if C[0] > C[1]:
                ...

        return -1
        # outside in .. hard to do
        # need to make choice, which way to go... maybe can be a DP problem?
        # let me try inside out.... it has to start with [0,1]
        # but it may TLE


class Solution:
    def findMaxLength(self, nums: List[int]) -> int:

        i1, j1 = 0, 1
        res = 0
        while j1 < len(nums):
            # to right
            l = 0
            i, j = i1, j1
            while j < len(nums) and {nums[i], nums[j]} == {0, 1}:
                l += 2
                i, j = i+2, j+2
            res = max(res, l)

            # to left
            l = 0
            i, j = i1, j1
            while i >= 0 and {nums[i], nums[j]} == {0, 1}:
                l += 2
                i, j = i-2, j-2
            res = max(res, l)

            # to left and right
            l = 0
            i, j = i1, j1
            while i >= 0 and j < len(nums) and {nums[i], nums[j]} == {0, 1}:
                l += 2
                i, j = i-1, j+1
            res = max(res, l)

            i1, j1 = i1+1, j1+1

        return res


"""
didn't expect it to work
[0,0,1,0,0,0,1,1] failed already 

12 / 564 test cases passed.
return to the DP solution
"""


class Solution:
    def findMaxLength(self, nums: List[int]) -> int:
        C = Counter(nums)
        res = 0

        def helper(l, r):
            if l == r:
                return
            if C[1] == C[0]:
                nonlocal res
                res = max(res, r-l+1)
                return

            # remove l
            C[nums[l]] -= 1
            helper(l+1, r)
            C[nums[l]] += 1
            # remoove r
            C[nums[r]] -= 1
            helper(l, r-1)
            C[nums[r]] += 1

        helper(0, len(nums)-1)
        return res


'''
of coz, TLE
[0,1,0,1,1,1,0,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,1,0,0,0,1,0,1,0,0,1,0,1,1,1,1,1,1,0,0,0,0,1,0,0,0,1,1,1,0,1,0,0,1,1,1,1,1,0,0,1,1,1,1,0,0,1,0,1,1,0,0,0,0,0,0,1,0,1,0,1,1,0,0,1,1,0,1,1,1,1,0,1,1,0,0,0,1,1]
didn't get very far
12 / 564 test cases passed.


okay.. antoher range sum usaga
0: -1
1: +1

then [0, 0, 1,0,0,0,1,1] becomes
[0, -1, -2, -1, -2,-3,-4,-3,-2]
-2 and -2, dist is 6... also 2, and 4 are valid too...
yeah...
'''


class Solution:
    def findMaxLength(self, nums: List[int]) -> int:
        nums = [0] + nums
        sumToPos = defaultdict(list)
        sumToPos[0].append(0)
        for i in range(1, len(nums)):
            nums[i] = nums[i-1] - 1 if nums[i] == 0 else nums[i-1] + 1
            sumToPos[nums[i]].append(i)

        res = 0
        for pos in sumToPos.values():
            if len(pos) > 1:
                res = max(res, pos[-1]-pos[0])

        return res


"""
Runtime: 848 ms, faster than 96.94% of Python3 online submissions for Contiguous Array.
Memory Usage: 23.3 MB, less than 5.01% of Python3 online submissions for Contiguous Array.
"""
