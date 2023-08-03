"""
https://leetcode.com/problems/maximum-size-subarray-sum-equals-k/?envType=study-plan&id=programming-skills-iii

I am thinking to range sum
then it becomes a two-sum problem(hashmap)
"""


from ast import List
from collections import defaultdict


class Solution:
    def maxSubArrayLen(self, nums: List[int], k: int) -> int:
        # want range-sum[i to j inclusive]  to be rangeSum[j] - rangeSum[i-1]
        # so a left padding

        presums = [0]*(len(nums)+1)
        sumToPos = defaultdict(int)
        for i in range(1, len(presums)):
            presums[i] = presums[i-1] + nums[i-1]
            sumToPos[presums[i]] = i

        res = 0
        for i in range(0, len(presums)):
            target = presums[i]+k
            if target in sumToPos:
                res = max(res, sumToPos[target]-i)

        return res
