"""
https://leetcode.com/problems/number-of-longest-increasing-subsequence/?envType=study-plan&id=dynamic-programming-ii

interesting, the ask is to find the number of LISs
1 <= nums.length <= 2000

so n**2 is no problem

let me see about that 
I can store the LIS for each i.. then at the end search for max

I can also do some binary search 

"""


from collections import Counter
from typing import List


class Solution:
    def findNumberOfLIS(self, nums: List[int]) -> int:

        dp = [1] * len(nums)
        for i,num in enumerate(nums):
            if i == 0:
                continue
            for j in range(i, -1, -1):
                if num > nums[j]:
                    dp[i] = max(dp[i], dp[j]+1)

        C = Counter(dp)
        prod = 1
        for c in C:
            prod *=c
        
        return prod

"""
failed at [1,3,5,4,7]
okay,
quickly I am educated 
dp [1, 2, 3, 3, 4]
so actually maybe I should be doing 
C[4] * C[3] * C[2] * C[1]


then failed at [1,2,4,3,5,4,7,2]
[1, 2, 3, 3, 4, 4, 5, 2]

okay.. 5 has two path
but 4 has only one path.

so cannot really do the prod
rethink... 

let dp to represnt the number of LIS
any element is itself a LIS so 1 is default

maybe I keep two elements in this dp
[lisLen, count]
"""


class Solution:
    def findNumberOfLIS(self, nums: List[int]) -> int:

        dp = [(1, 1)] * len(nums)
        maxLis = 1
        for j, num in enumerate(nums):
            if j == 0:
                continue
            lis = 1
            count = 1
            for i in range(j-1, -1, -1):
                preLis, prevCount = dp[i]
                if num > nums[i]:
                    if preLis + 1 > lis:
                        lis = preLis + 1
                        count = prevCount
                    elif preLis + 1 == lis:
                        # this is tricky
                        count += prevCount

            dp[j] = (lis, count)
            maxLis = max(maxLis, lis)

        return sum([count for lis, count in dp if lis == maxLis])

"""
Runtime: 1003 ms, faster than 88.12% of Python3 online submissions for Number of Longest Increasing Subsequence.
Memory Usage: 14.1 MB, less than 96.69% of Python3 online submissions for Number of Longest Increasing Subsequence.

not bad but let me see can I do better?

if I maintain the lis... 
I only need the longest.. 
which means ...

1 3  7 <- incoming 6, I can replace it with 1 3 6 but what use of it?

okay... 

not 100%, not even 80% but this problem deserves some more digging 
I see many good discussions 

I'll revisit
"""



if __name__ == '__main__':
    s = Solution()
    print(s.findNumberOfLIS([1,2,4,3,5,4,7,2]))