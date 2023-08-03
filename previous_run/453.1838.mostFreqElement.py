"""
https://leetcode.com/problems/frequency-of-the-most-frequent-element/

ok.. this one was not attempted yet
medium but <40% acceptance ratio.. could be tricky

ah.. nah.. I should have done it..
it is in a different session now

so this is actually a sliding window problem
no need the binary search part
"""


from typing import List


class Solution:
    def maxFrequency(self, nums: List[int], k: int) -> int:
        nums.sort()

        windSum = 0
        i=j=0
        res = 1

        while j<len(nums):
            windSum += nums[j]
            while (j-i+1)*nums[j] > windSum+k:
                windSum -= nums[i]
                i+=1 
            res = max(res, j-i+1)
            j+=1
        return res

"""
notice the sorting is O(n lgn)
so if there is a binary search solution that go thru the array in O(n)
and search for that element in O(lgn) time

could it do? without another sorting?

where is the montonicity?
given k:
    if some number meets the requirements
    will the smaller number meets? nah
    will the bigger number meets? maybe?
so not really a binary search problem 


so the binary search is like sort/prefix-sum/.. go-from-here

it's kind of troublesome and inefficient but a good thinking exercise..

https://leetcode.com/problems/frequency-of-the-most-frequent-element/discuss/1175181/JavaPython-Prefix-Sum-and-Binary-Search-O(NlogN)

idea:
    sort
    for each index,
        serach in [0,index] the smallest mid(sub-index) to meet adding K and windSum+k>=nums[index]*winLen
        this does has monotonicity
        if at i it meets, at any j>i it also meets..
    
"""

