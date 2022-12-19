"""
https://leetcode.com/problems/count-of-smaller-numbers-after-self/

this is a hard problem
not much idea...

but brute force is very clear O(n^2)

then I am thinking, this has some DP property
solve it using sub-problem

not quite but at least I can start with right.. which is 0.. 
then going to left

then I think maybe I can maintain an insert list

[4,5,3,4,3,2,1]
the list grows like 
1                   -> so it will 0..
1,2                 -> 2 will inserted at index-1, so it will be 1
1,2,3               -> 3 will be inserted at index-2, so it will be 2
1,2,3,4             -> 4:3
1,2,3,4 enter 3     -> so I need to bisect_right... it will be 3
1,2,3,3,4 enter 5   -> 5:5
1,2,3,3,4,5 enter 4 -> 4:4

so roughly it kind of check out
"""


from typing import List
from sortedcontainers import SortedList


class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        sl = SortedList()

        i = len(nums)-1
        while i >= 0:
            idx = sl.bisect_left(nums[i])
            sl.add(nums[i])
            nums[i] = idx
            i -= 1

        return nums


"""
so I want to use that BI tree to do this 

1. turn each number into ranking (what about the equal case???)
    maybe read this number-1's ranking-accumulation 
2. from right to left, 
    with its ranking reading the sum under num's-ranking 
    then update the BI Tree 



"""


class Solution:
    def countSmaller(self, nums: List[int]) -> List[int]:
        # store number and index for ranking calc
        numIdx = sorted([[n, i] for i, n in enumerate(nums)])
        rankings = [0]*len(nums)

        ranking = 1
        i = 0
        while i < len(numIdx):
            if i > 0 and numIdx[i][0] != numIdx[i-1][0]:
                ranking += 1

            rankings[numIdx[i][1]] = ranking
            i += 1

        bitree = [0]*(len(nums)+1)
        j = len(nums)-1
        while j >= 0:
            writeRank = readRank = rankings[j]
            # read my accu-rank in bi-tree
            accRank = 0
            readRank -= 1
            while readRank > 0:
                accRank += bitree[readRank]
                lsb = readRank & -readRank
                readRank -= lsb
            # no need for used elemet again so I can re-use this list to store final results
            rankings[j] = accRank

            # update my acc-rank in bi-tree
            while writeRank <= len(nums):
                bitree[writeRank] += 1
                lsb = writeRank & -writeRank
                writeRank += lsb

            j -= 1

        return rankings


"""
Runtime: 9050 ms, faster than 12.81% of Python3 online submissions for Count of Smaller Numbers After Self.
Memory Usage: 40.9 MB, less than 33.62% of Python3 online submissions for Count of Smaller Numbers After Self.
"""

if __name__ == '__main__':
    s = Solution()
    print(s.countSmaller([5, 2, 6, 1]))
    print(s.countSmaller([5, 1, 2, 6, 1]))
