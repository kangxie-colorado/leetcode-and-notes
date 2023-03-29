"""
https://leetcode.com/problems/cherry-pickup-ii/?envType=study-plan&id=dynamic-programming-iii

yeah.. this seems easier than cherry pick I
so just dfs down with memeorization

the states:
1. row.. each time the robot must move down a row so row is same for both
2. col1, col2.. 

f(r,c1,c2):
    so how many can be picked up 
    it has each 3 sub cases. 
    c1-1,c1,c1+1
    *
    c2-1,c2,c2+1

    we need to get the max of such 9 sub problems...
    and of course plus my current cell's cherry 
    if c1==c2: then +=grid[r][c1]
    else: +=grid[r][c1] +=grid[r][c2]

    base:
        out of bounds.. return -1
        reach the last row.. return results
    


"""


from functools import cache
from typing import List


class Solution:
    def cherryPickup(self, grid: List[List[int]]) -> int:
        m,n = len(grid), len(grid[0])

        @cache
        def f(r, c1,c2):
            if r >= m:
                return 0
            
            if c1<0 or c1>=n or c2<0 or c2>=n:
                return -1
            
            res = grid[r][c1]
            if c1 != c2:
                res += grid[r][c2]
            
            below = 0
            for i in (-1,0,1):
                for j in (-1,0,1):
                    below = max(below, f(r+1,c1+i,c2+j))
            
            res += below 
            return res
        
        return f(0,0,n-1)

"""
Runtime: 1216 ms, faster than 82.86% of Python3 online submissions for Cherry Pickup II.
Memory Usage: 49.7 MB, less than 20.57% of Python3 online submissions for Cherry Pickup II.
"""