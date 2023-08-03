"""
https://leetcode.com/problems/minimum-absolute-sum-difference/?envType=study-plan&id=binary-search-ii

I have forgotten how this was solved totally so I read the notes 
now I think 

the origDiffSum is fixed
absSumDiff(A,B) = sum ([abs(a-b) for a,b in zip(A,B)])

replace one num in A to minimize this diff means
brute force:
    for each a, we can have n-1 choices 
    we could try one by one 

or do we?
    observe there are some monotonicity in this 
        e.g. b is 3, a is 7.. you got other a as 5 9 10 11.. then 5 is closest to 3; 7 9 11 is even further 
    if we can reach some sorted state, we might get some time saving
        notice the diff is the distance, so find the closes one(s) in the sorted array could provide the smallest diff

with that in mind
    1. combine A and B and sort it by a (because we are search b in A for closest)
    2. look left/right for smaller dist
    go thru all of the pair
    this will O(n lgn)

"""


import bisect
from typing import List


class Solution:
    def minAbsoluteSumDiff(self, A: List[int], B: List[int]) -> int:
        mod = 10**9 + 7
        n = len(A)
        origSumDiff = sum([abs(a-b) for a,b in zip(A,B)])
        AB = sorted([(a,b) for a,b in zip(A,B)])

        res = float('inf')
        for a,b in AB:
            idx = bisect.bisect_left(AB,(b,0))

            leftAVal = AB[idx-1][0] if idx >= 0 else float('inf')
            rightAVal = AB[idx][0] if idx<n else float('inf')

            origDiff = abs(b-a)
            newDiff = min(abs(b-leftAVal), abs(b-rightAVal))
            res = min(res, origSumDiff - origDiff + newDiff)

        return res % mod