from collections import deque
from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        m, n = len(grid), len(grid[0])
        res = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '1':
                    res +=1 
                    # sink all adjacent ones
                    q = deque()
                    q.append((i,j))

                    while q:
                        x,y = q.popleft()
                        if grid[x][y] == '0':
                            continue
                        grid[x][y] = '0'

                        for dx,dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                            nx,ny = x+dx, y+dy
                            if 0<=nx<m and 0<=ny<n:
                                q.append((nx,ny))
        return res
