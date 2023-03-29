"""
https://leetcode.com/problems/number-of-corner-rectangles/?envType=study-plan&id=dynamic-programming-iii

not seem to have a very good algorithm?
just to start at any point, extend 3 ways until one end becomes exhausted?

hmm... 
"""


from collections import defaultdict
from typing import List


class Solution:
    def countCornerRectangles(self, grid: List[List[int]]) -> int:
        m,n = len(grid), len(grid[0])

        def countCornorRectFrom(x,y):
            x1 = x+1
            y1 = y+1
            res = 0
            while x1<m and y1<n:
                res += grid[x1][y] and grid[x][y1] and grid[x1][y1]
                x1,y1 = x1+1, y1+1
                
            return res

        res = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j]:
                    res += countCornorRectFrom(i,j)
        
        return res
"""

ah .. wait.. it is asking for rectangle
not sqare.. I was aiming to sqaure...

so I am thinking brute force?
find each such rect between any two rows.. 


"""


class Solution:
    def countCornerRectangles(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        def between(r1,r2):
            row1,row2 = grid[r1], grid[r2]
            res = 0
            for i in range(n):
                for j in range(i+1, n):
                    if row1[i] and row1[j] and row2[i] and row2[j]:
                        res += 1
            return res

        res = 0
        for i in range(m):
            for j in range(i+1,m):
                res += between(i,j)


        return res


class Solution:
    def countCornerRectangles(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        onesPerRow =  defaultdict(set)

        for i in range(m):
            for j in range(n):
                if grid[i][j]:
                    onesPerRow[i].add(j)
        
        res = 0
        for i in range(m):
            for j in range(i+1,m):
                sameOnes = len(onesPerRow[i].intersection(onesPerRow[j]))
                res += sameOnes*(sameOnes-1)//2

        return res
    
"""
Runtime: 658 ms, faster than 95.19% of Python3 online submissions for Number Of Corner Rectangles.
Memory Usage: 14.9 MB, less than 89.42% of Python3 online submissions for Number Of Corner Rectangles.
"""

if __name__ == '__main__':
    s = Solution()
    print(s.countCornerRectangles(grid = [[1,0,0,1,0],[0,0,1,0,1],[0,0,0,1,0],[1,0,1,0,1]]))
    print(s.countCornerRectangles(grid = [[1,1,1],[1,1,1],[1,1,1]]))