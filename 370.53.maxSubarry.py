"""
https://leetcode.com/problems/maximum-subarray/


did this before but still ran into nails..
kind of subtle.. not sure if I can come up with this in a stressful interview environment 
"""


from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:

        prefixSum = nums[0]
        s = nums[0]
        for num in nums[1:]:
            s = max(s, prefixSum+num, num) # either w/ or w/o prefixSum
            prefixSum = max(prefixSum+num, num, 0) # either taking current num+prefix, or only current num, or nothing

        return s


"""
lets see the divide and conquer approach? prefix sum again?

  [5,4,-1,7,8]
[0,5,9,8,15,23]

  [-2,1,-3,4,-1,2,1,-5,4]
[0,-2,-1,-4,0,-1,1,2,-3,1] the max - min max is to the right of min.. 

not divide and conquer 

I guess divide and conquer if finding left max subarray and right max subarray 
and the max subarray cross middle line??

yes

https://leetcode.com/problems/maximum-subarray/discuss/1595195/C%2B%2BPython-7-Simple-Solutions-w-Explanation-or-Brute-Force-%2B-DP-%2B-Kadane-%2B-Divide-and-Conquer

class Solution:
    def maxSubArray(self, nums):
        def maxSubArray(A, L, R):
            if L > R: return -inf
            mid, left_sum, right_sum, cur_sum = (L + R) // 2, 0, 0, 0
            for i in range(mid-1, L-1, -1):
                left_sum = max(left_sum, cur_sum := cur_sum + A[i])
            cur_sum = 0
            for i in range(mid+1, R+1):
                right_sum = max(right_sum, cur_sum := cur_sum + A[i])
            return max(maxSubArray(A, L, mid-1), maxSubArray(A, mid+1, R), left_sum + A[mid] + right_sum)
        return maxSubArray(nums, 0, len(nums)-1)

the cross mid, sum is just adding everything together and see how big it can retain
            for i in range(mid-1, L-1, -1):
                left_sum = max(left_sum, cur_sum := cur_sum + A[i])
            cur_sum = 0
            for i in range(mid+1, R+1):
                right_sum = max(right_sum, cur_sum := cur_sum + A[i])

also it can be precomputed.. pretty smart...

"""