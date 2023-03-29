"""
https://leetcode.com/problems/allocate-mailboxes/?envType=study-plan&id=dynamic-programming-iii

interesting problem 
so if there is only one mailbox k=1
then it has to be placed in the middle of far-left and far-right to minimize the distance 
nah.. that is not true...

[4,5,8,10,20]
1

10 is the best place 

hints are 
- If k =1, the minimum distance is obtained allocating the mailbox in the median of the array houses.
- Generalize this idea, using dynamic programming allocating k mailboxes.

okay glad I peeked at it.. otherwise I would be lost and have no idea it is median..

but knowing this, what is the outlet?
how to get the median of an sorted array?

like [4,5,8,10,20] .. 
it is 8... okay.. 
then for [4,5,8,10,12,20] it should be 9 and the total dist should be 25? yes, it is

okay.. median for k==1
now generalize this idea..

okay. .then it becomes that maxNumberOfEvent problem

f(idx,k) represent at idx 0, k left box to allocate 
    for each idx, it can be a group itself 
        f(idx+1, k-1)
    or it can form a group with next one
        f(idx+1, k)
hmm... not that smiliar

okay.. finding k medians in the array
the more mailbox, the smaller the minimum distances.. so we'd for sure use up all mailbox
that means, when left == k, we just install a mailbox to each house to make them 0... 

and the dist to median can be computed by prefixSum.. if we need 

back to f(idx,k):
    but what it represents?
        current group ends at idx? and k mailbox left?
    maybe represent 
        1. i can let current group ends at idx, between last ending and this one, I put a mailbox
            f(idx+1,k-1)
        2. i can continue to grow current box, 
            f(idx+1,k)
    
    problem is then I need to keep track of previous ending to calculate?
    or actually.. hmmm... maybe I use a start of the group.. an end of the group to track.. 
    because in the way I can cache

f(s,e,k): s,e: start and end of group
    if cut off here:
        [s,e] inclusive? generate a dist 
        dist(s,e) + f(e+1,e+1,k-1)
    continue to grow:
        f(s,e+1,k)

I guess could have a try 


"""


from functools import cache
from typing import List


class Solution:
    def minDistance(self, houses: List[int], k: int) -> int:
        n = len(houses)
        houses.sort()
        prefixSum = [0]*(n+1)
        for i in range(1,n+1):
            prefixSum[i] = prefixSum[i-1] + houses[i-1]

        def groupDist(groupStart, groupEnd):
            l = groupEnd-groupStart+1
            if l % 2 == 0:
                # even number elements
                m1 = groupStart + (groupEnd-groupStart)//2
                m2 = m1+1
                median = (houses[m1] + houses[m2])//2
                leftDist = (m1-groupStart+1)*median - \
                    (prefixSum[m1+1]-prefixSum[groupStart])
                rightDist = (prefixSum[groupEnd+1] -
                             prefixSum[m2]) - (groupEnd-m2+1)*median
            else:
                m = groupStart + (groupEnd-groupStart)//2
                median = houses[m]
                leftDist = (m-groupStart+1)*median - \
                    (prefixSum[m+1]-prefixSum[groupStart])
                rightDist = (prefixSum[groupEnd+1] -
                             prefixSum[m]) - (groupEnd-m+1)*median
            return leftDist + rightDist

        @cache
        def f(groupStart, groupEnd, leftMailboxs):
            if groupEnd == n:
                return float('inf')

            if n-groupStart <= leftMailboxs:
                # we can install a mailbox to each house already
                return 0
            
            if leftMailboxs == 1:
                # only one box left.. all the rest houses must share!
                return groupDist(groupStart, n-1)

            # continue to grow or use current section as a group
            return min(
                f(groupStart, groupEnd+1, leftMailboxs),
                f(groupEnd+1, groupEnd+1, leftMailboxs-1) + groupDist(groupStart, groupEnd)
            )
        
        return f(0,0,k)


"""
Runtime: 827 ms, faster than 36.18% of Python3 online submissions for Allocate Mailboxes.
Memory Usage: 94.3 MB, less than 6.53% of Python3 online submissions for Allocate Mailboxes.
"""

if __name__ == '__main__':
    s = Solution()
    
    print(s.minDistance(houses = [1,4,8,10,20], k = 1))
    print(s.minDistance(houses = [1,4,8,10,20], k = 3))

    print(s.minDistance(houses = [2,3,5,12,18], k = 2))

    houses = [147, 59, 125, 19, 22, 21, 181, 189, 66, 12, 93, 55, 131, 112, 28,
         132, 101, 108, 155, 107, 154, 52, 11, 16, 128, 124, 165, 84, 194]
    k = 23
    print(s.minDistance(houses, k))
