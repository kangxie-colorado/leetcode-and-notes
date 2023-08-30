"""
each step, 9 choices???
"""

from functools import cache
from typing import List


class Solution:
    def cherryPickup(self, grid: List[List[int]]) -> int:
        rows,cols = len(grid), len(grid[0])

        @cache
        def f(r, c1, c2):
            if c1<0 or c1>=cols or c2<0 or c2>=cols:
                return 0
            pickup = (grid[r][c1] + grid[r][c2]) if c1!=c2 else grid[r][c1]
            if r == rows-1:
                return pickup
            
            return pickup + max(f(r+1,c1-1,c2), 
                                f(r+1,c1,c2),
                                f(r+1,c1+1,c2),
                                f(r+1,c1-1,c2-1), 
                                f(r+1,c1,c2-1),
                                f(r+1,c1+1,c2-1),
                                f(r+1,c1-1,c2+1), 
                                f(r+1,c1,c2+1),
                                f(r+1,c1+1,c2+1),
                                )
        
        return f(0,0,cols-1)



            
            