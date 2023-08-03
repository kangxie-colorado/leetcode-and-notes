"""
https://leetcode.com/problems/partition-equal-subset-sum/

I did this before in go
but now that cannot pass...

but I guess the nature of the problem is the same why it fails now
so I know this is still a knapsack problem

I am going to take or not-take any element to form the half sum
"""


from functools import cache
from typing import List


class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        summ = sum(nums)
        if summ % 2 != 0:
            return False
        target = summ//2

        @cache
        def f(idx, total):
            if total == target:
                return True

            if total > target or idx >= len(nums):
                return False

            # take or not-take
            return f(idx+1, total+nums[idx]) or f(idx+1, total)

        return f(0, 0)

"""
Runtime: 921 ms, faster than 77.49% of Python3 online submissions for Partition Equal Subset Sum.
Memory Usage: 154.3 MB, less than 10.30% of Python3 online submissions for Partition Equal Subset Sum.

with cache 

okay the failed was something I didn't understand either and I wrote

/**
How does this one work?
**/


okay... now let me see the bottom up
two dimension 

idx and total.. 

[1,5,11,5]
    0  1 2 3 4 5 6 7 8 9 10 11
1
5
11
5

dp[i][j] - represents using upto i-th element, can a total j be formed 
from the recursive function definition 
idx depends on idx+1 --- meaning it is likely to scan from bottom up
total??? to say it depends on total+some-num, maybe not that right.. 
because the function can be written to seek total becomes zero (remain)

let me see

"""


class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        summ = sum(nums)
        if summ % 2 != 0:
            return False
        target = summ//2

        @cache
        def f(idx, remain):
            if remain == 0:
                return True

            if remain < 0  or idx >= len(nums):
                return False

            # take or not-take
            return f(idx+1, remain-nums[idx]) or f(idx+1, remain)

        return f(0, target)

"""
Runtime: 871 ms, faster than 78.87% of Python3 online submissions for Partition Equal Subset Sum.
Memory Usage: 154.4 MB, less than 10.30% of Python3 online submissions for Partition Equal Subset Sum.

so yeah, as remain, it might tell the logical relationship clearer 

[1,5,11,5]
    0  1 2 3 4 5 6 7 8 9 10 11
1
5
11
5

do now dp[i][j] can be true if {
    dp[i+1][j] is true
    dp[i+1][j-A[i]] is true
}

still not super right..
the end result will be in the right/bottom corner
however I want to start here???

actually the problem is symmetric so start from the end is okay too
"""


class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        summ = sum(nums)
        if summ % 2 != 0:
            return False
        target = summ//2

        @cache
        def f(idx, remain):
            if remain == 0:
                return True

            if remain < 0 or idx < 0:
                return False

            # take or not-take
            return f(idx-1, remain-nums[idx]) or f(idx-1, remain)

        return f(len(nums)-1, target)

"""
Runtime: 388 ms, faster than 94.55% of Python3 online submissions for Partition Equal Subset Sum.
Memory Usage: 79.3 MB, less than 20.43% of Python3 online submissions for Partition Equal Subset Sum.

hmm.. so this problem doesn't necessarily has a clear profile, which way depends on the other way?
it is a symmetric problem.. only for the convienience 

Now the following seems true

[1,5,11,5]
    0  1 2 3 4 5 6 7 8 9 10 11
N   T  F F F F F F F F F F F     <-- I need to initialize it to this?
1
5
11
5

do now dp[i][j] can be true if {
    dp[i-1][j] is true
    dp[i-1][j-A[i]] is true
}

notices it only relies on last row..
therefore it can be one row only

"""


class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        summ = sum(nums)
        if summ % 2 != 0:
            return False
        target = summ//2

        dp = [[0]*(target+1) for _ in range(len(nums)+1)]
        dp[0][0] = 1

        for i in range(1, len(nums)+1):
            for j in range(target+1):
                if j == 0:
                    dp[i][j] = 0
                    continue

                dp[i][j] |= dp[i-1][j]
                if j >= nums[i-1]:
                    dp[i][j] |= dp[i-1][j-nums[i-1]]
                
                if j==target and dp[i][j]:
                    return True
        return dp[len(nums)][target]

"""
Runtime: 5692 ms, faster than 12.42% of Python3 online submissions for Partition Equal Subset Sum.
Memory Usage: 29.8 MB, less than 40.36% of Python3 online submissions for Partition Equal Subset Sum.

uh..oh.. so much slower???
early termination??

adding such to try
                
                if j==target and dp[i][j]:
                    return True
Runtime: 3893 ms, faster than 23.55% of Python3 online submissions for Partition Equal Subset Sum.
Memory Usage: 29.8 MB, less than 41.25% of Python3 online submissions for Partition Equal Subset Sum.

hmm... let me see that one-row dp
I kind of forgot do I need to reverse iterating the nums?
or somehow??

but this needs to scan from right to left
why not left to right? I don't remember --- because if you change the dependency first, you change the end result
that is why the 2-D or 2-row keep that state extra

this row's dp[j] depends on last row's dp[j-NUM] not this row's dp[j-NUM]
from left to right scan one row if you change dp[j-NUM] first... you have changed dp[j] as well

but the dependency don't have to be dp[j] -> dp[j+NUM] so we can do dp[j] first
it can be that way if we model it that way.. so this is just confusion/conflicts avoiding
"""


class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        summ = sum(nums)
        if summ % 2 != 0:
            return False
        target = summ//2

        dp = [0]*(target+1) 
        dp[0] = 1

        # for num in nums[::-1]: # reverse is the same: symmetric 
        for num in nums:
            for j in range(target,-1,-1):

                # dp[i][j] |= dp[i-1][j] # this is now default inheritance
                if j >= num:
                    dp[j] |= dp[j-num]

                if j == target and dp[j]:
                    return True
        return dp[target]

"""
Runtime: 1554 ms, faster than 59.01% of Python3 online submissions for Partition Equal Subset Sum.
Memory Usage: 13.9 MB, less than 96.85% of Python3 online submissions for Partition Equal Subset Sum.

consider they added new cases... so it is understandable
        for num in nums[::-1]:

"""