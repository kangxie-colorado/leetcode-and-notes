"""
https://leetcode.com/problems/search-in-rotated-sorted-array-ii/?envType=study-plan&id=binary-search-ii

I sovled this a few times already but not very smoothly each and every time 

After solving another problem, that is using l,r to reprent the length and the idx is deducted from that
I think I could borrow that idea

1. find the true min - minIdx
2. lo=minIdx, hi=(minIdx+l-1)%l (or mindIdx+l-1)
search in this range.. 
m = lo + (hi-lo)//2 
but now the m need to % len()
"""


from typing import List

"""
failed 
[1,0,1,1,1]
0

hmm...
okay.. this is problem II in this series..
I was doing the first problem https://leetcode.com/problems/search-in-rotated-sorted-array/description/

class Solution:
    def search(self, nums: List[int], target: int) -> bool:
        n = len(nums)
        # search for min idx
        lo, hi = 0, n-1
        while lo < hi:
            mi = lo+(hi-lo)//2
            if nums[mi] < nums[-1]:
                hi = mi
            else:
                lo = mi + 1
        minIdx = lo

        lo, hi = minIdx, minIdx + n-1
        while lo < hi:
            mi = lo+(hi-lo)//2
            if nums[mi % n] < target:
                lo = mi+1
            else:
                hi = mi

        return lo%n if nums[lo%n]==target else -1

yeah.. the code indeed works for that
Runtime: 42 ms, faster than 87.72% of Python3 online submissions for Search in Rotated Sorted Array.
Memory Usage: 14.2 MB, less than 53.67% of Python3 online submissions for Search in Rotated Sorted Array.

okay played a while back to this issue
if I can find the min idx.. I can still do the same

because binary search works on sorted array containing duplicates too 
so the 2nd part no need to change.. 

let me see the first part 

        while lo < hi:
            mi = lo+(hi-lo)//2
            if nums[mi] < nums[-1]:
                # if <, then min is still upto mi
                hi = mi
            elif nums[mi] > nums[-1]:
                # if >. then the min can only be in the right half
                lo = mi + 1
            else:
                # if =, that is complicated
                # it means nums[mi] to num[hi] are equal 
                # then it can be or to the left
                hi = mi 
        minIdx = lo

    this logic didn't check out
    [1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1]



"""


class Solution:
    def search(self, nums: List[int], target: int) -> bool:
        n = len(nums)
        # search for min idx
        lo, hi = 0, len(nums)-1
        while lo < hi:
            mi = lo+(hi-lo)//2
            if nums[mi] < nums[hi]:
                # if <, then min is still upto mi
                hi = mi
            elif nums[mi] > nums[hi]:
                # if >. then the min can only be in the right half
                lo = mi + 1
            else:
                # if =, that is complicated
                # it means two cases:
                #  1. all num between nums[mi] to num[right] are equal - and this number has a chance to be the min
                #       thus I can continue until the first e.g  0 1 1 1  -> 0 1 1 1 (i.e. rid of right number)
                #  2. some smaller number are in between 1 1 1 1 0 1 1 ... 
                #       thus I can continue until 0... 
                #  3. some bigger number are in between 1 1 1 1 2 1 1...
                #       thus I can continue to 1...
                #  but to generalize I'd better to continue if and only if nums[hi]==nums[hi-1]
                #  otherwise, I rid of a left 
                if hi>0 and nums[hi]==nums[hi-1]:
                    hi -= 1
                else:
                    # 1 1 1 2 1
                    #         hi
                    # mid is 1, so it cannot be 2 1 1 2 1.. not sorted 
                    # i.e. if nums[hi-1] != nums[hi]
                    # that means nums[hi] --wrap--> nums[mi] are all the same.. 
                    # kind of hard to say that but just a feeling.. and it worked
                    lo+=1
        minIdx = lo

        lo, hi = minIdx, minIdx + len(nums)-1
        while lo < hi:
            mi = lo+(hi-lo)//2
            if nums[mi % n] < target:
                lo = mi+1
            else:
                hi = mi

        return nums[lo % n] == target

"""
Runtime: 59 ms, faster than 74.21% of Python3 online submissions for Search in Rotated Sorted Array II.
Memory Usage: 14.4 MB, less than 92.02% of Python3 online submissions for Search in Rotated Sorted Array II.

Runtime: 54 ms, faster than 90.43% of Python3 online submissions for Search in Rotated Sorted Array II.
Memory Usage: 14.4 MB, less than 56.65% of Python3 online submissions for Search in Rotated Sorted Array II.

okay.. then I look at this problem

https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/?envType=study-plan&id=binary-search-ii

class Solution:
    def findMin(self, nums: List[int]) -> int:
        l, r = 0, len(nums)-1

        while l < r:
            m = l+(r-l)//2

            if nums[m] > nums[r]:
                # get rid of the left
                l = m+1
            elif nums[m] < nums[r]:
                # get rid of the right
                r = m
            else:  # nums[m] == nums[r]
                # get rid of the right element
                r -= 1

        return nums[l]
I was wondering where my idea of getting rid of an element coming from 
it is from here

and I can see.. while this is right to find the minimum but not right to find the minimum's idx.

so changed it to this

class Solution:
    def findMin(self, nums: List[int]) -> int:
        l, r = 0, len(nums)-1

        while l < r:
            m = l+(r-l)//2

            if nums[m] > nums[r]:
                # get rid of the left
                l = m+1
            elif nums[m] < nums[r]:
                # get rid of the right
                r = m
            else:  # nums[m] == nums[r]
                # get rid of the right element
                if r>0 and nums[r]==nums[r-1]:
                    r-=1
                else:
                    l+=1

        return nums[l]

still works
Runtime: 51 ms, faster than 93.42% of Python3 online submissions for Find Minimum in Rotated Sorted Array II.
Memory Usage: 14.4 MB, less than 39.69% of Python3 online submissions for Find Minimum in Rotated Sorted Array II.

"""

if __name__ == '__main__':
    s = Solution()
    a = [1, 0, 1, 1, 1]
    t = 0

    print(s.search(a,t))