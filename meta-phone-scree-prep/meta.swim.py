
"""
of course I solved this before and I still don't know how now

bfs.
at t, push everything I can reach to q using a dfs 
if dest is discovered, then output t

otherwise, incr t and do another round
"""


from collections import deque
from functools import cache
import heapq
from typing import List


class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        
        t = 0
        q = deque([0,0])

        while q:
            x,y = q.popleft()

            # I have visited this
            if grid[x][y] < t:
                ...

"""
cannot continue this thought train

think other angles
it is actually to find a path, where the top of this path is smallest possible 

I can use a heap to discover next step, and for each next step, see if it can reach the end with that t
"""                

class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)

        dfs_visited = set()
        @cache
        def reachDest(t, x,y):
            if (x,y) == (n-1,n-1):
                return True
            
            dfs_visited.add((x,y))

            for dx,dy in [(-1,0), [1,0], [0,-1], [0,1]]:
                nx,ny = x+dx, y+dy
                if (nx,ny) in dfs_visited:
                    continue
                if 0<=nx<n and 0<=ny<n and grid[nx][ny]<= t and reachDest(t, nx,ny):
                    return True

            return False

        h = []
        heapq.heappush(h, (grid[0][0], 0,0))
        visited = set()
        while h:
            t,x,y = heapq.heappop(h)
            if (x,y) in visited:
                continue
            visited.add((x,y))

            if reachDest(grid[x][y], x,y):
                return t

            for dx,dy in [(-1,0), [1,0], [0,-1], [0,1]]:
                nx,ny = x+dx, y+dy
                if 0<=nx<n and 0<=ny<n:
                    heapq.heappush(h, (grid[nx][ny], nx,ny))

"""
okay, still wrong understanding...
this is a lesson, before understand it thoroughly, don't jump in
"""


if __name__ == '__main__':
    s = Solution()
    print(s.swimInWater( grid = [[3,2],[0,1]]))
    print(s.swimInWater([[11,15,3,2],[6,4,0,13],[5,8,9,10],[1,14,12,7]]))
    print(s.swimInWater( grid = [[0,2],[1,3]]))
    print(s.swimInWater(grid = [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]))