"""
for each land, discover its neighbor land
and update the region's outlines...
"""

from collections import deque
from typing import List


class Solution:
    def closedIsland(self, grid: List[List[int]]) -> int:
        m,n = len(grid), len(grid[0])        
        res = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] == 0:
                    up, down, left, right = m,-1,n,-1
                    q = deque()
                    q.append((r,c))
                    while q:
                        x,y = q.popleft()
                        grid[x][y] = -1
                        up,down,left,right = min(up, x), max(down, x), min(left, y), max(right, y)
                        for dx,dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                            nx,ny = x+dx, y+dy
                            if 0<=nx<m and 0<=ny<n and grid[nx][ny]==0:
                                q.append((nx,ny))
                    if 0<up<m-1 and 0<down<m-1 and 0<left<n-1 and 0<right<n-1:
                        res += 1
        return res

                        
if __name__ == '__main__':
    s = Solution()
    print(s.closedIsland(grid = [[1,1,1,1,1,1,1,0],[1,0,0,0,0,1,1,0],[1,0,1,0,1,1,1,0],[1,0,0,0,0,1,0,1],[1,1,1,1,1,1,1,0]]))


