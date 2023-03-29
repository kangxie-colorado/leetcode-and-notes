"""
https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/?envType=study-plan&id=dynamic-programming-iii

hmm..
if I sort out all the overlapps? 
and start from the most overlapped interval.. take as many as I can?

ah.. I see, in example 1: there are three overlaps that have two ballons 
but if you shot the 2nd, it will leave leftmost and rightmost ballon alone

so I can choose to shot anyway.. and inside a ballon's range it makes no different than I can just shot at the edge 
or when the number of ballon change..

for this one: Input: points = [[10,16],[2,8],[1,6],[7,12]]

if I do a line sweeping..

ballon loc: 1 2 6 7 8 10 12 16  <-- the ending loc is a bit tricky.. how to mark it
ballon cnt: 1 2 2 2 2 2  2  1

for each loc, I can choose to shot one or not.. 
lets say if I shot at x=2
    then two ballons are popped... I will be left with two ballon to deal with.. and 

seems like based on this I can make a desicion 
....

went for a walk.. 
thinking the situations.. email about lexinton vistas project.. helped someone find a disc golf
the possible relationship.. just so many things..

and this problem
it might not be that deciscion based walk thru

think in another way:
    the leftmost ballon.. must be shot by an arrow no later than its end 
    then we take as many as ballon with me... 

that left it a sub problem.. right?
I guess we can try 

at least the examples check out fine


"""


import bisect
from typing import List


class Solution:
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        points.sort()
        res = 0
        idx = 0
        while idx < len(points):
            # shot at its end and search for all overlapping ballons 
            search = [points[idx][1], float('inf')]
            idx = bisect.bisect_left(points,search)
            res += 1
        
        return res

"""
okay.. didn't go far
[[9,12],[1,10],[4,11],[8,12],[3,9],[6,9],[6,7]]
1 vs 2

al right.. after sorting
[[1, 10], [3, 9], [4, 11], [6, 7], [6, 9], [8, 12], [9, 12]]
you shot at 10.. 3.9 will be fine..

hmm...
so I sort by end??? and search for start?
would I be facing the same issue?

"""


class Solution:
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        points.sort(key=lambda x:x[1])
        res = 0
        i = 0
        while i < len(points):
            # shot at its end and search for all overlapping ballons
            j=i+1
            while j<len(points) and points[j][0]<=points[i][1]:
                j+=1
            
            i=j
            res+=1

        return res

"""
Runtime: 1360 ms, faster than 88.43% of Python3 online submissions for Minimum Number of Arrows to Burst Balloons.
Memory Usage: 59.9 MB, less than 34.42% of Python3 online submissions for Minimum Number of Arrows to Burst Balloons.

so okay.. not actually binary search.. just two pointer to go thru
and greedy part is focusing on the leftmost ballon, which is the first ballon to disappear from shotting range if you don't act
"""