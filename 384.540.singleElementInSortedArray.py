"""
https://leetcode.com/problems/single-element-in-a-sorted-array/

all but one number appear exactly twice
one number appear exactly once
so it must be odd number of elements in total

taking the first mid, it will be landing on a even-idx 
0-3: 1, 0-5:2 0-9:4
and that single number cannot land on the even idx.. simply because other number take two spots at a time

and sorted.. so it creates a condition to search the odd size half... 

if A[m] == A[m-1], the number is in the left including m
if A[m] == A[m+1], the number is in the right not including m

but will it out of bounds

hmm.. not right yet

1 2 2
    m = 1, A[1] == A[2] but in the left side 
    so okay.. it also depends on the odd/even of m
    if m is odd, and A[m] == A[m+1], that means in the left side there are odd numbers, r=m-1

    if m is even, e.g. 1 1 2 2 3, that means in the left side there are even numbers and I am at left side of my numbers
    so it has to be in the right, l=m+2

1 1 2
    for A[1] == A[0], I am at the right side of my own numbers.
     if m is odd, that means the left-to-m is even, must at the right side l = m+1
     
     1 2 2 3 3, if m is even that means the right to m is even, must at the left side, r = m-2

"""


from typing import List


class Solution:
    def singleNonDuplicate(self, nums: List[int]) -> int:
        # the l,r represents where this number could be
        l,r = 0,len(nums)-1

        while l<r:
            m = l+(r-l)//2
            leftVal = nums[m-1] if m>0 else -1
            rightVal = nums[m+1] if m<len(nums)-1 else -1

            if nums[m]!=leftVal and nums[m] != rightVal:
                return nums[m]

            if nums[m]==leftVal:
                # I am at the right side of my own numbers 
                if m%2==0:
                    r = m-2
                else:
                    l = m+1
            
            if nums[m]==rightVal:
                # I am at the left side of my own numbers
                if m%2==0:
                    l = m+2
                else:
                    r = m-1
            
        return nums[l]

"""
Runtime: 172 ms, faster than 94.29% of Python3 online submissions for Single Element in a Sorted Array.
Memory Usage: 23.8 MB, less than 16.54% of Python3 online submissions for Single Element in a Sorted Array.

still kind of messy 
this solution is actually good but many people have problem
https://leetcode.com/problems/single-element-in-a-sorted-array/discuss/100754/Java-Binary-Search-short-(7l)-O(log(n))-w-explanations

it has a trick... that is in the solution titled as

Approach 3: Binary Search on Evens Indexes Only
hmm... maybe I can only search for even indexs 

[1,1,2,3,3,4,4,8,8]

what if I only search index [0,2,4,6,8]

m = 4, compare to m+1, 
    equal then? search right -  [1,1,2,2,3,3,4,8,8] l=m+2
    not equal then? search left - [1,1,2,3,3,4,4,8,8] r=m also [1,1,2,2,3,4,4,8,8]

yeah.. how do I model this? exactly like this 
        if mid % 2 == 1:
            mid -= 1
    hmm... 
"""
