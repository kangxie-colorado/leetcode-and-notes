"""
https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/

I did this with SortedList
then I see https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/discuss/609771/JavaC%2B%2BPython-Deques-O(N)

the deque idea is genius and let me code it up
the idea seems simple
1. keep a decreasing deque for the max: which keeps the max in the window to the front
    when a bigger value arrives, pop until it is not bigger than the tail element
2. keep a increasing deque for the min: which keeps the min in the window to the front
    when a smaller values arrives, pop until it is not smaller than the tail element
3. why pop-front can make the window valid again
    because the maxDQ keeps the biggest value to front, upon its leaving.. the diff will become smaller
    minDQ keeps the smallest value to front, and same effect

4. because we don't pop the equal value.. so the values itself can be used to tell a front-element to pop
5. Lee used the non shrinking tech.. I am going to do shrinking first



"""


from collections import deque
from typing import List


class Solution:
    def longestSubarray(self, nums: List[int], limit: int) -> int:
        res = i = j = 0
        maxQ = deque()
        minQ = deque()
        while j < len(nums):

            # enqueue
            while maxQ and maxQ[-1] < nums[j]:
                maxQ.pop()
            maxQ.append(nums[j])

            while minQ and minQ[-1] > nums[j]:
                minQ.pop()
            minQ.append(nums[j])

            while maxQ[0] - minQ[0] > limit:
                if nums[i] == maxQ[0]:
                    maxQ.popleft()
                if nums[i] == minQ[0]:
                    minQ.popleft()

                i += 1

            res = max(res, j-i+1)
            j += 1

        return res


"""
Runtime: 1660 ms, faster than 57.10% of Python3 online submissions for Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit.
Memory Usage: 23.2 MB, less than 90.36% of Python3 online submissions for Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit.

now the non-shrinking one
"""


class Solution:
    def longestSubarray(self, nums: List[int], limit: int) -> int:
        res = i = j = 0
        maxQ = deque()
        minQ = deque()
        while j < len(nums):

            # enqueue
            while maxQ and maxQ[-1] < nums[j]:
                maxQ.pop()
            maxQ.append(nums[j])

            while minQ and minQ[-1] > nums[j]:
                minQ.pop()
            minQ.append(nums[j])

            if maxQ[0] - minQ[0] > limit:
                if nums[i] == maxQ[0]:
                    maxQ.popleft()
                if nums[i] == minQ[0]:
                    minQ.popleft()

                i += 1
            j += 1

        return j-i


"""
Runtime: 1745 ms, faster than 52.75% of Python3 online submissions for Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit.
Memory Usage: 23.9 MB, less than 50.95% of Python3 online submissions for Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit.

holy shit.. just like that..
"""
