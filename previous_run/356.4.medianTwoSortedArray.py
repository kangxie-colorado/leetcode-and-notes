"""
https://leetcode.com/problems/median-of-two-sorted-arrays/

I solved this but quite messy
I have listened to NeetCode's solution 

this is "search the range" type of binary search... 
I didn't understand much now hope I do

the idea is search for a left partition 
total 13 number, then I search for 6 left in the left

the generic way of doing that is 
search in the shorted array.. 

say I have n element, n//2 as the left partion.. 
A: [0, n//2... n-1] -> [0...n//2] for the left partition 
then 
B: [0, (m+n)//2-n//2...m-1] -> [0...m//2] will be the left partion

if this matches then depending on the odd/even total number count.. we can deduce the answer
otherwise, adjust the range accordingly

how do I adjust the range, by adjusting m.. 
[0..m] both inclusive will be the left partion

if the range is too small.. then I l=m+1 and recalculate the m.. thus a new range..

also if the A is downsized to empty.. a trick to deal with it is to padding a absolute min/max to each end
keep that in mind

"""


from typing import List


class Solution:
    def findMedianSortedArrays(self, A: List[int], B: List[int]) -> float:
        bigVal = 10000000
        if len(A) > len(B):
            A,B = B,A
        A = [-bigVal] + A + [bigVal]
        B = [-bigVal] + B + [bigVal]
        sizeA, sizeB = len(A), len(B)
        leftParSize = (sizeA+sizeB)//2

        l,r = 0,sizeA-1
        
        # we will always have a median.. l<r probably isn't right or necessary
        while True:
            # partition from A is [0..parA], parA+1 is its size
            parA = l + (r-l)//2
            parB = leftParSize - (parA + 1) - 1 # minus 1 to get the idx

            # this is the right partition
            if A[parA] <= B[parB+1] and B[parB] <= A[parA+1]:
                if (sizeA+sizeB)%2==0:
                    return (max(A[parA], B[parB]) + min(A[parA+1], B[parB+1]))/2
                else:
                    return min(A[parA+1], B[parB+1])
            elif A[parA] > B[parB+1]:
                # e.g.
                # A [1,7,8,9]               [1,7]
                # B [1,2,3,4,5,6,7,8]       [1,2,3,4]
                # A[parA] = 7 > B[parB+1]=5
                # so 7 cannot be in left partion
                # parA is too big, cannot include it
                r = parA - 1
            else:
                # e.g.
                # A [1,1,2,3]               [1,1]
                # B [2,3,4,5,6,7,8,9]       [2,3,4,5]
                # A[parA+1] = 2 < B[parB]=5
                # so left-partition in A must go further right
                # if we do l=m.. it might not move at all
                l = parA + 1


"""
let me think

A [1,2,3,4]
B [5,6,7,8,9,10,11,12,13]

this way.. the parA could go to 4 and get out of bound.. 
also 

A [21,22,23,24]
B [5,6,7,8,9,10,11,12,13]

it could also go out of left bound
so yeah the padding is convienient and easy

but doesn't it make it O(m)???
maybe array copy can be done all at once?

padding both A and B

Runtime: 103 ms, faster than 79.19% of Python3 online submissions for Median of Two Sorted Arrays.
Memory Usage: 14.1 MB, less than 97.10% of Python3 online submissions for Median of Two Sorted Arrays.

Runtime: 99 ms, faster than 85.31% of Python3 online submissions for Median of Two Sorted Arrays.
Memory Usage: 14.2 MB, less than 66.65% of Python3 online submissions for Median of Two Sorted Arrays.


"""

# let me see if I don't pad
class Solution:
    def findMedianSortedArrays(self, A: List[int], B: List[int]) -> float:
        bigVal = 10000000

        leftParSize = (len(A)+len(B))//2
        even = (len(A)+len(B)) % 2 == 0

        if not A or not B:
            C = A or B
            return (C[leftParSize] + C[leftParSize-1])/2 if even else C[leftParSize]

        # handle non-overlapping 
        def nonOverlap(A,B):
            assert A[-1] <= B[0]
            if leftParSize < len(A):
                return (A[leftParSize] + A[leftParSize-1])/2 if even else A[leftParSize]
            elif leftParSize == len(A):
                return (A[-1] + B[0])/2 if even else B[0]
            else:
                rightParSize = leftParSize-len(A)
                return (B[rightParSize] + B[rightParSize-1])/2 if even else B[rightParSize-1]
        
        if A[-1] <= B[0]:
            return nonOverlap(A,B)
        if B[-1] <= A[0]:
            return nonOverlap(B,A)
                    
        if len(A) > len(B):
            A, B = B, A
        l, r = 0, len(A)-1
        # we will always have a median.. l<r probably isn't right or necessary
        while True:
            # if l>r:
                # A is totally wasted 
                # meaning A is totally bigger than B
                # so the median has to be in B, at most A[0] could take a part
                # same edge case could go to A is totall smaller than B
                # therefore.. these two cased can be handled upfront
                # as a matter of fact, it is not handled by those edge cases
                # e.g. [3] and [1,2,4], the r will be come -1 next step
                # this is getting super complicated
                # the padding is essentical here.
                # just no idea is padding makes it O(N) already

            # partition from A is [0..parA], parA+1 is its size
            parA = l + (r-l)//2
            parB = leftParSize - (parA + 1) - 1  # minus 1 to get the idx

            # this is the right partition
            nextInA = A[parA+1] if parA+1 < len(A) else bigVal
            nextInB = B[parB+1] if parB+1 < len(B) else bigVal
            if A[parA] <= nextInB and B[parB] <= nextInA:
                if even:
                    return (max(A[parA], B[parB]) + min(nextInA, nextInB))/2
                else:
                    return min(nextInA, nextInB)
            elif A[parA] > nextInB:
                r = parA - 1
            else:
                l = parA + 1


"""
aha... I wasn't thinking enough and paying attention 
there is no need to really pad.. but conceptually padding 
"""


class Solution:
    def findMedianSortedArrays(self, A: List[int], B: List[int]) -> float:
        leftParSize = (len(A)+len(B))//2
        even = (len(A)+len(B)) % 2 == 0


        if len(A) > len(B):
            A, B = B, A
        l, r = 0, len(A)-1
        while True:
            # partition from A is [0..parA], parA+1 is its size
            i = l + (r-l)//2
            j = leftParSize - (i + 1) - 1  # minus 1 to get the idx

            # the things are i,j,i+1,j+1 could be out of bounds each of themm
            # so easy to mess up.. this falling-back-to-default saved my day
            # i will not >= len(A) because of i = l + (r-l)//2
            # but i indeed could <0... 
            # there are so many hidden tricks here...
            aLeft = A[i] if i >= 0 else float('-inf')
            aRight = A[i+1] if (i+1)<len(A) else float('inf') 
            bLeft = B[j] if j>=0 else float('-inf')
            bRight = B[j+1] if (j+1)<len(B) else float('inf')

            if aLeft <= bRight and bLeft <= aRight:
                if even:
                    return (max(aLeft, bLeft) + min(aRight, bRight))/2
                else:
                    return min(aRight, bRight)
            elif aLeft > bRight:
                r = i - 1
            else:
                l = i + 1
"""
Runtime: 92 ms, faster than 94.20% of Python3 online submissions for Median of Two Sorted Arrays.
Memory Usage: 14.2 MB, less than 24.12% of Python3 online submissions for Median of Two Sorted Arrays.

overall, this is a super good problem..
"""