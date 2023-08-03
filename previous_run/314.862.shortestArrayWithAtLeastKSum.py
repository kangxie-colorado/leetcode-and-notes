"""
https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/

I cannot crack it
reading 

https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/discuss/189039/Detailed-intuition-behind-Deque-solution

What does the Deque store :
The deque stores the possible values of the start pointer. Unlike the sliding window, values of the start variable will not necessarily be contiguous.


Why is it increasing :
So that when we move the start pointer and we violate the condition, we are sure we will violate it if we keep taking the other values from the Deque. In other words, if the sum of the subarray from start=first value in the deque to end is smaller than target, then the sum of the subarray from start=second value in the deque to end is necessarily smaller than target.
So because the Deque is increasing (B[d[0]] <= B[d[1]]), we have B[i] - B[d[0]] >= B[i] - B[d[1]], which means the sum of the subarray starting from d[0] is greater than the sum of the sub array starting from d[1].

^^ okay.. it is trying to form this mono-increasing form so can move start to for sure violate the condition 
the queus stores the possible start idxes, and among the idxes, they point to prefix sum.. the pointed sums are increasing 


Why using Deque and not simply an array :
We can use an array, however we will find ourselves doing only three operations:
1- remove_front : when we satisfy our condition and we want to move the start pointer
2- append_back : for any index that may be a future start pointer
3- remove_back : When we are no longer satisfying the increasing order of the array
Deque enables doing these 3 operations in a constant time.

^^ the #3 strikes me most
when the sum is not increasing... remove the back; it is not only not to get into queue
but get rid of the decreasing sequeces 
e.g. 
[-1,-2,-3, 1] -> whatever.. the first 3 are not needed in the queue

then e.g.
A = [2,-1,2,1] K=3
B = [0,2,1,3,4]
deque = [0]

on 2.. 
    - 2-0<3 so no need to popleft
    - 2>0... so no need to pop right
    deque = [(0,0),(1,2)] # idx, B[idx]

on 1..
    - 1-0<3 so no need to popleft
    - B[2(idx-2)]<=B[d[-1](which is idx1)], remove back
        - B[2] > B[0] so no need to remove furhter 
    deque = [(0,0),(2,1)]

on 3..
   - 3-0>=3.. d[0] which is 0 find its shortest, which is 3-0 = 3, popleft()
   deque = [(2,1)]
   - B[3] > B[2], it is increasing.. so append it
   deque = [(2,1), (3,3)]

on 4..
    - 4-1>=3 (why 1? it is from (idx-2, B[2]=1)).. the len is updated to 2
    - B[4]=4>B[3]=3, so no need to remove back
    deque = [(2,1), (3,3), (4,4)]
"""


from typing import Deque, List


class Solution:
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        nums = [0]+nums
        for i in range(1, len(nums)):
            nums[i] += nums[i-1]

        dq = Deque()

        j = 0
        res = len(nums)
        while j < len(nums):
            while dq and nums[j] - nums[dq[0]] >= k:
                res = min(res, j-dq.popleft())

            while dq and nums[j] <= nums[dq[-1]]:
                dq.pop()

            dq.append(j)
            j += 1

        return res if res < len(nums) else -1


"""
Runtime: 1997 ms, faster than 57.11% of Python3 online submissions for Shortest Subarray with Sum at Least K.
Memory Usage: 29.1 MB, less than 8.02% of Python3 online submissions for Shortest Subarray with Sum at Least K.
"""
