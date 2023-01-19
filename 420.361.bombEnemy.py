"""
https://leetcode.com/problems/bomb-enemy/

seems like I can just scan upwards/downwards/left/right 

"""


from typing import List


class Solution:
    def maxKilledEnemies(self, grid: List[List[str]]) -> int:
        m,n = len(grid), len(grid[0])
        # from left
        # can deal with from right as well
        left = [[0]*n for _ in range(m)]
        right = [[0]*n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '0':
                    left[i][j] = left[i][j-1] if j>0 else 0
                if grid[i][j] == 'E':
                    left[i][j] = left[i][j-1]+1 if j> 0 else 1
                if grid[i][j] == 'W':
                    left[i][j] = 0

                k = n-1-j
                if grid[i][k] == '0':
                    right[i][k] = right[i][k+1] if k < n-1 else 0
                if grid[i][k] == 'E':
                    right[i][k] = right[i][k+1]+1 if k < n-1 else 1
                if grid[i][k] == 'W':
                    right[i][k] = 0

        
        up = [[0]*n for _ in range(m)]
        down = [[0]*n for _ in range(m)]
        for j in range(n):
            for i in range(m):
                if grid[i][j] == '0':
                    up[i][j] = up[i-1][j] if i>0 else 0
                if grid[i][j] == 'E':
                    up[i][j] = up[i-1][j] +1 if i > 0 else 1
                if grid[i][j] == 'W':
                    up[i][j] = 0

                k = m-1-i
                if grid[k][j] == '0':
                    down[k][j] = down[k+1][j] if k < n-1 else 0
                if grid[k][j] == 'E':
                    down[k][j] = down[k+1][j]+1 if k < n-1 else 1
                if grid[k][j] == 'W':
                    down[k][j] = 0
        
        res = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '0':
                    res = max(res, up[i][j] + down[i][j] + left[i][j] + right[i][j])
        return res
