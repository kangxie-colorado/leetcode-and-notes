"""
https://leetcode.com/problems/max-consecutive-ones-ii/

ah.. this is 2nd installment of that serie.. 
no surprise I feel it so familiar

okay.. what I did is 
https://leetcode.com/problems/max-consecutive-ones-iii/submissions/

why this is a DP?
not sliding window

maybe both
"""


from typing import List


class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        i=j=0
        rSum = 0
        res = 0
        while j<len(nums):            
            rSum += nums[j]
            if rSum >= j-i:
                res = max(res, j-i+1)
            
            while i<j and rSum < j-i:
                rSum -= nums[i]
                i+=1
            
            j+=1

        return res

"""
Runtime: 459 ms, faster than 64.44% of Python3 online submissions for Max Consecutive Ones II.
Memory Usage: 14.3 MB, less than 72.60% of Python3 online submissions for Max Consecutive Ones II.

okay.. after some mind farts.. I cannot quickly figure out the structure of the code
it workded 
"""


class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        i = j = 0
        rSum = 0
        res = 0
        while j < len(nums):
            rSum += nums[j]

            while rSum < j-i:
                rSum -= nums[i]
                i += 1
            res = max(res, j-i+1)
            j += 1

        return res

"""
also this is right.. 
now, this is the most basic sliding window form

Runtime: 412 ms, faster than 80.76% of Python3 online submissions for Max Consecutive Ones II.
Memory Usage: 14.3 MB, less than 32.26% of Python3 online submissions for Max Consecutive Ones II.

"""


class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        i = j = 0
        rSum = 0
        res = 0
        while j < len(nums):
            rSum += nums[j]

            if rSum < j-i:
                rSum -= nums[i]
                i += 1
            j += 1

        return j-i

"""
Runtime: 385 ms, faster than 91.39% of Python3 online submissions for Max Consecutive Ones II.
Memory Usage: 14.4 MB, less than 32.26% of Python3 online submissions for Max Consecutive Ones II.


this is non-shrinking sliding window
now let me think the DP solution 

so maybe it depends on prev number is 0 or 1?
or current number is 1 or 0?

maybe two states steram
contain-0:
not-contain-0: 

then depends on curr val, 1 or 0
if currVal = 1:
    contain-0: max(dp[0][i-1]+1, dp[1][i-1]+1)
    not-contain-0: dp[1][i-1]+1 as well 

if currVal = 0:
    # this is interesting
    contain-0: cannot continue, dp[1][i-1]+1 # can flip myself and continue from not-contain-0 stream
    not-contain-0: this must go to 0, because this stream not-contain-0

              1   0   1   1   0
contain   0   1   2   3   4   3 <-this one is interesting , it is 3 not 4.. but the max is 4
not       0   1   0   1   2   0



              1   0   1   1   0   1
contain   0   1   2   3   4   3   4
not       0   1   0   1   2   0   1

okay.. so also at most I need two variables..



"""


class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        contain0 = 0
        notContain0 = 0
        res = 0

        for num in nums:
            if num == 1:
                contain0 +=  1
                notContain0 += 1
            else:
                contain0 = notContain0+1
                notContain0 = 0 
            res = max(res, contain0, notContain0)

        return res

"""
Runtime: 378 ms, faster than 92.89% of Python3 online submissions for Max Consecutive Ones II.
Memory Usage: 14.3 MB, less than 32.26% of Python3 online submissions for Max Consecutive Ones II.
"""