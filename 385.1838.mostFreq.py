"""
https://leetcode.com/problems/frequency-of-the-most-frequent-element/

another binary search which I did but kind of forgot
"""


from typing import List


class Solution:
    def maxFrequency(self, nums: List[int], k: int) -> int:
        nums.sort()

        def valid(m):
            # so I don't know here.. maybe sliding window
            # the sum + k, is it >= windown_len*the right numer
            # ahha.. that is it -- and that is is O(n)
            i=j=0
            summ = 0
            while j<len(nums):
                summ+=nums[j]
                
                if j-i+1==m:
                    if summ + k >= m*nums[j]:
                        return True
                    summ -= nums[i]
                    i+=1
                j+=1
            return False

        l,r = 1,len(nums)

        while l<r:
            # converge from left or converge from right
            # this is seek a max.. usually it should converge from right
            m = r-(r-l)//2
            if valid(m):
                l = m
            else:
                r = m-1
        return l

"""
Runtime: 4057 ms, faster than 25.04% of Python3 online submissions for Frequency of the Most Frequent Element.
Memory Usage: 27.9 MB, less than 64.14% of Python3 online submissions for Frequency of the Most Frequent Element.

ah.. after sorting.
this can be solved as a sliding window
"""

if __name__ == '__main__':
    print(Solution().maxFrequency( nums = [1,2,4], k = 5))