"""
just to go thru the island cells 
if it shares an edge with water (out of matrix or water), then this is an perimeter edge
otherwise, 
"""

from typing import List


class Solution:
    def islandPerimeter(self, grid: List[List[int]]) -> int:
        m,n = len(grid), len(grid[0])
        def isLand(x,y):
            return 0<=x<m and 0<=y<n and grid[x][y]
 
        perimeter = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j]:
                    # up
                    for dx,dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                        x,y = i+dx, j+dy
                        if not isLand(x,y):
                            perimeter += 1
        
        return perimeter