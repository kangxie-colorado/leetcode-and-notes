"""
not really very good ways to solve this

maybe just go one land by another
try reaching every house it can.. and record the minimal

if it cannot reach all the houses, then marked it -1, also marked its union -1
"""

from collections import deque
from typing import List


class Solution:
    def shortestDistance(self, grid: List[List[int]]) -> int:
        M,N = len(grid), len(grid[0])
        houses = set()
        for i in range(M):
            for j in range(N):
                if grid[i][j] == 1:
                    houses.add((i,j))
        
        def mhDist(r,c):
            res = 0
            for x,y in houses:
                res += abs(r-x) + abs(c-y)
            return res

        def minDistToHouses(r,c):
            q = deque()
            q.append((r,c, 0))
            visited = set()
            reachedHouse = {}

            steps = 0
            while q:                
                x,y,steps = q.popleft()
                
                if (x,y) in visited:
                    continue
                visited.add((x,y))

                for dx,dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nx,ny = x+dx, y+dy
                    if 0<=nx<M and 0<=ny<N:
                        if grid[nx][ny] == 2:
                            continue
                        if grid[nx][ny] == 1:
                            if (nx,ny) not in reachedHouse:
                               reachedHouse[(nx,ny)] = steps + 1
                            if steps + 1 < reachedHouse[(nx,ny)]:
                               reachedHouse[(nx,ny)] = steps+1
                              
                            continue
                        q.append((nx,ny,steps+1))
                
            if reachedHouse.keys() == houses:
                return sum(reachedHouse.values())
            return -1
        
        def markUnreachableCells(x,y):
            q = deque()
            q.append((x,y))
            while q:
                x,y = q.popleft()
                if grid[x][y] == -1:
                    continue
                grid[x][y] = -1
                for dx,dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nx,ny = x+dx, y+dy
                    if 0<=nx<M and 0<=ny<N and grid[nx][ny] == 0:
                        q.append((nx,ny))
        
        res = float('inf')
        for x in range(M):
            for y in range(N):
                if grid[x][y] == 0:
                    if mhDist(x,y) >= res:
                        continue
                    minDist = minDistToHouses(x,y)
                    if minDist == -1:
                        markUnreachableCells(x,y)
                        continue
                    res = min(res, minDist)
        
        return res if res != float('inf') else -1

if __name__ == '__main__':
    s = Solution()
    print(s.shortestDistance(grid = [[1,1,1,1,1,0],[0,0,0,0,0,1],[0,1,1,0,0,1],[1,0,0,1,0,1],[1,0,1,0,0,1],[1,0,0,0,0,1],[0,1,1,1,1,0]]))
    print(s.shortestDistance(grid = [[1,0,2,0,1],[0,0,0,0,0],[0,0,1,0,0]]))