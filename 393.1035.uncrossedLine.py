"""
https://leetcode.com/problems/uncrossed-lines/?envType=study-plan&id=dynamic-programming-ii

quite hard to think 
but I just did that LCS problem.. so I kind of see this as a LCS issue 
"""


from typing import List


class Solution:
    def maxUncrossedLines(self, nums1: List[int], nums2: List[int]) -> int:

        dp = [[0] * (len(nums2)+1) for _ in range(len(nums1)+1)]
        for i in range(1, len(nums1)+1):
            for j in range(2, len(nums2)+1):

                if nums1[i-1] == nums2[j-1]:
                    dp[i][j] = 1 + dp[i-1][j-1]
                
                dp[i][j] = max(dp[i][j], dp[i-1][j], dp[i][j-1])
        return dp[len(nums1)][len(nums2)]

"""
Runtime: 214 ms, faster than 75.07% of Python3 online submissions for Uncrossed Lines.
Memory Usage: 14.3 MB, less than 65.55% of Python3 online submissions for Uncrossed Lines.
"""
