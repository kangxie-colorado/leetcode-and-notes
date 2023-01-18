"""
https://leetcode.com/problems/largest-divisible-subset/?envType=study-plan&id=dynamic-programming-ii

sort and dp??
maybe O(n**2) can pass too
"""


from typing import List


class Solution:
    def largestDivisibleSubset(self, nums: List[int]) -> List[int]:
        nums.sort()
        dp = [1]*len(nums)
        maxLDS = 1
        maxIdx = -1
        for i in range(1,len(nums)):
            for j in range(0,i):
                if nums[i]%nums[j] == 0:
                    dp[i] = max(dp[i], dp[j]+1)
            if dp[i] > maxLDS:
                maxLDS = dp[i]
                maxIdx = i

        
        # now I search in the dp array for the subset
        j = maxIdx-1
        last = nums[maxIdx]
        res = [last]
        while j>=0:
            if dp[j] == maxLDS-1 and last%nums[j]==0:
                res.append(nums[j])
                last = nums[j]
                maxLDS -= 1
            j-=1

        return res[::-1]

"""
Runtime: 394 ms, faster than 81.82% of Python3 online submissions for Largest Divisible Subset.
Memory Usage: 14 MB, less than 96.26% of Python3 online submissions for Largest Divisible Subset.

hahha.. this getting the len and then reverse engineering is not bad
"""


if __name__ == '__main__':
    s = Solution()
    print(s.largestDivisibleSubset([1,2,3]))