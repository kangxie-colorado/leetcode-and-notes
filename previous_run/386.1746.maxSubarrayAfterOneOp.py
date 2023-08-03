"""
https://leetcode.com/problems/maximum-subarray-sum-after-one-operation/?envType=study-plan&id=dynamic-programming-ii

the acceptance is high 
but I see nothing


for every element, it can change or not change
so at least there is a O(n*n) solution 

for each element, I change it then I calculate the subarray max sum.. 
but of course that wont pass 

hmm.. thinking for a while.. no luck
it probably is a new knowledge point???

looking at the hints

- Think about dynamic programming
- Define an array dp[nums.length][2], where dp[i][0] is the max subarray sum including nums[i] and without squaring any element.
- dp[i][1] is the max subarray sum including nums[i] and having only one element squared.

ah.. see a glimpse
still two states..


okay.. I see
the key word is "including" nums[i] not "up to" nums[i]
[2,-1,-4,-3]
including -1, means [2,-1] [-1]
including -4, means [2,-1,4] [-1,-4] [-4]

therefore it reminds me of the other problem https://leetcode.com/problems/maximum-subarray/
in that one, as long as the previous sum is >0, I can continue to accumulate the sum  
otherwise, I just be myself 
when updating the result, apply the sum to num sum+num.. *this is including nums[i]*

note the sum is the running sum including the nums[i]
but actually the code below deviates from that meaning already anyway.. continue after the code

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        
        sum = 0
        res = -100000
        for num in nums:
            res = max(res, sum+num)
            sum = max(sum+num, 0)
        
        return s

    // sum, the max possible sum so far
    // either postive or 0, meaning prefix is negative so start with the current number
    // it gets rid of negative prefix automatically


for this problem

dp[0][i] will be the max subarray sum including nums[i], (which means ending at nums[i])
dp[1][i] will be the max subarray sum including nums[i] and with one element squared 

    dp[1][i] vs dp[*][i-1]:
        I can square myself, thus 
            if dp[0][i-1]>0, I can add up to it; or I will just be my sqaure 
        I can use some previous square, thus 
            if dp[1][i-1]>0, I can add up to it; or I will just be my self
    
    dp[0][i] vs dp[*][i-1]:
        this is the subarray sum of orig stream.. so no need to concern the dp[1][i-1]
        the rule will be 
            if dp[0][i-1]>0, I can add up to it.. otherwise, I just be myself

as usual.. two variables are enough 

"""


from typing import List


class Solution:
    def maxSumAfterOperation(self, nums: List[int]) -> int:

        regMax = 0
        squareOneMax = 0
        res = float('-inf')
        for num in nums:
            # if regMaxSum>0:
            #     regMaxSum+=num
            # else:
            #     regMaxSum = num
            # this is just equal to 
            # note I didn't use dp rows.. so at least using a new variable to avoid the cross impacts
            newRegMax = max(regMax+num, num)
            
            # I just use myself as a start
            # newSqureOneMax = num 
            # if sqaureOneMaxSum > 0:
            #     # if I use the sum with a prev element squared and it is positive I can add up to it
            #     newSqureOneMax = sqaureOneMaxSum + num
            # # I can just square myself...
            # newSqureOneMax = max(newSqureOneMax, num*num)
            # if regMaxSum > 0:
            #     # I can choose regular sum and square myself
            #     newSqureOneMax = max(newSqureOneMax, regMaxSum+num*num)
            # this is just equal to
            newSqureOneMax = max(num, squareOneMax + num, regMax+num*num, num*num)

            res = max(res, newRegMax, newSqureOneMax)
            regMax = newRegMax
            squareOneMax = newSqureOneMax
        return res

"""
Runtime: 1052 ms, faster than 90.00% of Python3 online submissions for Maximum Subarray Sum After One Operation.
Memory Usage: 27.6 MB, less than 93.08% of Python3 online submissions for Maximum Subarray Sum After One Operation.


using the same thinking to solve https://leetcode.com/problems/maximum-subarray/

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        
        summ = 0
        res = float('-inf')
        for num in nums:
            # only one regular sum compared to problem.1746
            # just reuse the same varible
            summ = max(summ+num, num)
            res = max(res, summ)
        
        return res
"""

if __name__ == '__main__':
    s = Solution()
    nums = [2,-1,-4,-3]
    print(s.maxSumAfterOperation(nums))  #17

    nums = [1,-1,1,1,-1,-1,1]
    print(s.maxSumAfterOperation(nums))  #4