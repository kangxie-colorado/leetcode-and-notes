"""
knap-sack problem

"""

from functools import cache
from typing import List


class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        S = sum(nums)
        if S % 2 !=0:
            return False
        target = S//2

        @cache
        def f(i,remain):
            if remain == 0:
                return True
            if i>=len(nums):
                return False
            
            return f(i+1, remain) or f(i+1, remain-nums[i])
        
        return f(0,target)