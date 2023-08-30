"""
not hard to see
1. sort it (acutlaly no need, it say subarray, so must be in original nums)
2. when discover a seq of 3
  the 4th will contribute 2
  the 5th will contribute 3..
  and so on... 
because when [a b c d] is arithmetic, [b c d] must be
"""

from typing import List


class Solution:
    def numberOfArithmeticSlices(self, nums: List[int]) -> int:
        i=2
        res = 0
        while i<len(nums):
            if not ((nums[i] - nums[i-1]) == (nums[i-1] - nums[i-2])):
                i+=1
                continue
            
            delta = nums[i] - nums[i-1]
            j=i
            while j < len(nums) and (nums[j] - nums[j-1]) == delta:
                res += j-i+1
                j+=1
            i = j

        return res
        
