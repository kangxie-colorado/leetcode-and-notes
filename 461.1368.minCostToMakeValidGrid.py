"""
https://leetcode.com/problems/minimum-cost-to-make-at-least-one-valid-path-in-a-grid/?envType=study-plan&id=graph-ii

hmm.. dp?
starting from the end 0

going to left.. 
    if it points to it..  dp[i][j-1] -> dp[i][j] (arrow 1)
        dp[i][j-1] = dp[i][j]
        otherwise dp[i][j-1] + 1
    when left is exhausted
    going up one row??

example 2 deniest this simple theory

dp[i][j] = min (
    dir1: the cell it points to 
    1 + dir2/dir3/dir4
)

how to avoid the pingpong dependencies?
think I can borrow what I learned in the maze problem.. if the cost getting bigger..?

not much idea.. let me code some and see if other ideas come up 

"""


from collections import defaultdict
from functools import cache
import heapq
from typing import List


class Solution:
    def minCost(self, grid: List[List[int]]) -> int:
        m,n = len(grid), len(grid[0])
        cost = [[m+n]*n for _ in range(m)]
        cost[m-1][n-1] = 0

        dirs = {
            (0,1): 1,
            (0,-1): 2,
            (1,0): 3,
            (-1,0): 4
        }

        res = float('inf')
        visited = defaultdict(int)
        def dfs(x,y):
            if visited[x,y] == 1:
                return float('inf')
            
            # 1: in the dfs path so far
            visited[x,y] = 1
            if (x,y) == (m-1,n-1):
                nonlocal res
                return 0
            
            for (dx,dy),arrow in dirs.items():
                if 0<=dx+x<m and 0<=dy+y<n:
                    if arrow == grid[x][y]:
                        cost[x][y] = min(cost[x][y], dfs(x+dx,y+dy))
                    else:
                        cost[x][y] = min(cost[x][y], dfs(x+dx,y+dy)+1)
            
            # all the options exhausted
            visited[x,y] = 2
            return cost[x][y]

        dfs(0,0)
        return cost[0][0]


"""
okay.. quick it errors out.
the visited logic is not that right..

a neighbor cell can be visited in different paths..
so 1/2 to diff?

okay.. still not right..
put the path into the function
"""


class Solution:
    def minCost(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        cost = [[m+n]*n for _ in range(m)]
        cost[m-1][n-1] = 0

        dirs = {
            (0, 1): 1,
            (0, -1): 2,
            (1, 0): 3,
            (-1, 0): 4
        }

        def dfs(x, y, path):
            if (x,y) in path:
                return float('inf')

            if (x, y) == (m-1, n-1):
                return 0

            path.add((x,y))
            for (dx, dy), arrow in dirs.items():
                if 0 <= dx+x < m and 0 <= dy+y < n:
                    if arrow == grid[x][y]:
                        cost[x][y] = min(cost[x][y], dfs(x+dx, y+dy, path))
                    else:
                        cost[x][y] = min(cost[x][y], dfs(
                            x+dx, y+dy, path)+1)
            path.remove((x,y))

            # all the options exhausted
            return cost[x][y]

        dfs(0, 0, set())
        return cost[0][0]

"""
21 cases passed 
failed at a complext one
using leetcode "debugger" to help find a small case to debug

[[3,4,3],[2,2,2],[2,1,4],[2,2,4],[2,1,3],[1,2,1],[4,3,2],[3,3,4],[2,2,1]]


okay.. fixed the error but TLE as expected
cannot cache becasue path is un-hashable

okay.. I guess dfs is not a viable option at all..

let me see how to improve????

bfs???? take all the 0 zeros.. in 
process them.. 
then cost 1s..


"""


class Solution:
    def minCost(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dirs = {
            (0, 1): 1,
            (0, -1): 2,
            (1, 0): 3,
            (-1, 0): 4
        }

        h = []
        heapq.heappush(h, (0,0,0)) # cost, x,y
        # thinking if you go back.. that will make the cost higher so never got seleteced
        # the change only once implicitly means this... somehow?
        visited = set()
        while h:
            cost,x,y = heapq.heappop(h)
            if (x,y) == (m-1,n-1):
                return cost 
            
            visited.add((x,y))

            for (dx,dy), arrow in dirs.items():
                nx,ny = x+dx, y+dy
                if 0 <= nx < m and 0 <= ny < n and (nx,ny) not in visited:
                    if arrow == grid[x][y]:
                        heapq.heappush(h,(cost,nx,ny))
                    else:
                        heapq.heappush(h,(cost+1, nx,ny))

"""
okay.. 47 / 68 test cases passed.
TLE

but results is right.. 
okay.. bfs layer by layer.. use set for each layer to save time?


"""


class Solution:
    def minCost(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        dirs = {
            (0, 1): 1,
            (0, -1): 2,
            (1, 0): 3,
            (-1, 0): 4
        }
        directions = {
            v:k for k,v in dirs.items()
        }

        def getEqualSet(startX, startY):
            equalCostSet = set()
            x,y=startX, startY
            while 0<=x<m and 0<=y<n and (x,y) not in equalCostSet:
                equalCostSet.add((x,y))
                dx,dy = directions[grid[x][y]]
                x+=dx
                y+=dy
            return equalCostSet  

        equalCostSet = getEqualSet(0,0)

        everProcessed = set()
        cost = 0
        while True:
            nextCostSet = set()
            for x,y in equalCostSet:
                if (x,y) == (m-1,n-1):
                    return cost 
                for dx, dy in dirs:
                    nx,ny = x+dx, y+dy
                    if 0 <= nx < m and 0 <= ny < n and (nx,ny) not in equalCostSet and (nx,ny) not in everProcessed:
                        nextSet = getEqualSet(nx, ny)
                        for node in nextSet:
                            if node not in equalCostSet and node not in everProcessed:
                                nextCostSet.add(node)

                everProcessed.add((x,y))

            equalCostSet = nextCostSet
            cost += 1 


"""
Runtime: 485 ms, faster than 52.97% of Python3 online submissions for Minimum Cost to Make at Least One Valid Path in a Grid.
Memory Usage: 15.6 MB, less than 80.62% of Python3 online submissions for Minimum Cost to Make at Least One Valid Path in a Grid.
"""

if __name__ == '__main__':
    s = Solution()
    print(
        s.minCost([[1, 2, 1, 1], [2, 2, 2, 2], [1, 3, 4, 1], [2, 1, 2, 3]])) # 3
    print(s.minCost(grid = [[1,1,3],[3,2,2],[1,1,4]])) # 0
    print(s.minCost(grid = [[1,2],[4,3]])) # 1
    print(
        s.minCost(grid=[[1, 1, 1, 1], [2, 2, 2, 2], [1, 1, 1, 1], [2, 2, 2, 2]])) # 3
    print(s.minCost(grid=[[3, 4, 3], [2, 2, 2], [2, 1, 4], [2, 2, 4], [
          2, 1, 3], [1, 2, 1], [4, 3, 2], [3, 3, 4], [2, 2, 1]])) # 6
    print(
        s.minCost([[1, 2, 1, 1], [2, 2, 2, 2], [1, 3, 4, 1], [2, 1, 2, 3]]))
    
    print(s.minCost(grid=[[1, 2, 1, 1], [2, 2, 2, 2], [1, 1, 4, 1], [2, 2, 2, 2]]))

    a= [[3,4,3],[2,2,2],[2,1,1],[4,3,2],[2,1,4],[2,4,1],[3,3,3],[1,4,2],[4,1,4],[2,1,4],[3,2,2],[1,2,3]]
    print(s.minCost(a)) # 9

    a = [[2,2,3,3,4,4,4,3,1,1,1,3,3,2,2,1,4,2,1,3,1,2,4,1,2,4,3,1,3,1,1,1,3],[4,3,2,1,3,4,3,3,1,4,3,4,4,4,3,3,2,1,2,2,2,3,2,4,1,2,2,2,1,3,4,1,1],[4,1,3,4,1,1,3,3,3,3,2,1,1,2,4,4,4,1,4,2,4,1,4,1,1,3,3,1,2,2,1,2,2],[1,3,3,4,4,1,3,1,3,3,2,4,3,4,4,4,3,3,1,3,1,1,1,4,3,4,4,1,4,3,4,2,1],[1,1,1,2,2,3,3,1,3,1,2,2,3,4,4,4,1,2,1,3,1,4,1,4,1,2,4,4,4,3,4,4,3],[1,4,2,3,3,2,1,4,2,1,2,1,4,1,2,1,1,3,2,2,3,2,3,4,2,1,1,2,4,3,3,3,4],[2,3,2,1,2,3,4,2,2,1,3,4,4,3,2,2,3,4,4,1,3,1,4,3,4,4,3,1,2,3,3,4,4],[2,3,1,1,4,4,3,3,3,3,1,1,3,3,3,1,1,1,4,1,3,1,2,1,2,1,2,3,2,2,3,1,3],[4,2,2,2,1,1,4,4,2,4,2,4,1,1,2,4,4,2,4,1,2,3,3,1,3,1,3,1,4,1,1,4,1],[3,4,3,2,4,4,2,3,2,2,3,4,2,4,2,4,2,4,4,2,4,1,2,2,2,2,1,4,2,3,3,2,3],[4,3,1,1,2,4,2,3,2,1,4,2,3,3,4,3,2,3,1,2,1,3,2,3,2,1,1,2,4,4,3,1,2],[1,3,2,1,3,4,1,2,1,2,1,1,2,4,4,4,1,2,2,2,4,1,3,1,1,1,3,2,2,2,2,2,1],[1,4,3,3,4,4,3,4,2,1,2,3,1,4,4,3,3,3,2,3,4,3,1,4,4,4,4,1,4,2,3,4,2],[3,2,2,2,1,4,4,2,3,2,2,3,4,1,4,4,3,2,1,1,4,2,3,1,3,1,1,3,1,4,2,1,3],[3,4,3,3,3,2,4,1,2,3,1,3,2,2,4,2,4,4,2,3,1,3,2,2,4,3,1,3,1,3,2,4,3],[4,1,1,3,3,1,4,2,3,4,1,2,1,4,2,4,3,2,4,2,2,3,3,3,3,3,2,4,2,2,4,4,1],[3,2,1,4,1,4,4,1,3,1,4,4,2,2,4,1,1,1,2,1,3,3,4,1,3,4,3,1,3,4,1,1,3],[1,3,2,3,3,3,4,4,2,4,1,1,3,2,1,1,1,1,2,1,1,2,1,2,4,1,4,1,1,2,1,3,4],[3,3,4,1,3,4,3,3,2,3,2,3,3,4,4,2,1,3,1,4,4,1,4,1,1,1,4,3,2,2,1,4,4],[3,4,1,1,1,2,4,2,4,2,1,1,2,3,3,1,3,4,1,2,3,4,4,4,2,1,4,3,4,3,4,4,2],[3,1,3,2,3,3,1,1,3,2,1,3,2,3,4,4,2,3,1,2,3,4,1,3,2,4,3,4,2,3,2,4,4],[2,1,4,4,3,4,2,1,3,3,4,2,3,1,1,2,1,2,2,2,2,1,1,4,1,3,3,3,4,2,1,2,3],[4,3,2,4,1,3,3,3,3,4,4,4,1,3,1,1,2,2,3,4,1,3,3,3,1,3,4,3,1,4,4,2,4],[2,2,2,4,4,1,3,3,2,2,3,1,4,1,3,4,4,4,4,2,1,3,3,2,4,3,2,1,1,2,3,2,3],[4,2,1,2,4,4,1,2,2,4,2,1,2,4,2,3,1,1,4,1,4,1,4,2,3,4,1,2,4,3,2,3,2],[1,3,1,2,4,3,3,3,2,4,3,1,3,3,3,3,4,3,2,2,3,1,1,1,4,1,3,3,3,2,4,1,3],[3,1,2,3,2,3,1,2,2,3,1,3,2,2,3,4,4,1,3,2,1,3,2,4,1,4,3,4,3,4,3,4,3],[4,4,3,3,3,4,3,2,3,3,2,4,2,2,1,3,2,3,1,4,4,2,2,4,2,3,3,3,4,1,3,4,4],[1,1,1,2,1,4,2,1,1,1,1,4,2,4,1,2,1,2,4,3,2,1,4,2,2,3,4,2,4,1,3,3,2],[3,1,3,1,1,3,2,1,3,3,4,4,4,3,2,3,3,1,4,1,4,1,4,3,4,1,4,3,1,1,4,2,1],[3,1,1,4,3,2,4,2,2,3,2,2,4,4,3,4,1,4,4,4,3,3,4,4,1,2,4,4,1,4,1,2,3],[4,3,1,2,3,1,4,3,2,1,3,1,3,4,1,3,4,3,1,3,1,2,3,2,2,1,2,4,4,1,3,3,3],[4,3,3,3,3,2,1,3,1,3,4,1,1,1,3,3,2,1,2,2,3,2,4,3,2,1,2,2,4,4,1,3,2],[2,3,3,2,2,1,3,1,3,2,2,4,1,4,1,2,2,2,4,3,3,1,1,4,2,3,3,3,4,4,4,4,4],[3,2,4,2,3,4,3,2,2,1,4,1,2,2,2,4,3,2,2,4,4,4,3,3,2,1,4,4,1,1,4,3,1],[1,1,3,2,4,3,1,3,2,2,3,4,1,2,3,1,3,3,2,1,3,2,4,1,2,1,2,4,2,1,4,3,3],[3,1,3,4,4,3,1,1,4,4,1,3,4,4,1,2,4,1,1,3,4,2,2,3,2,1,1,2,3,4,4,1,1],[3,2,4,4,1,4,2,3,1,4,3,1,2,4,3,3,1,1,4,1,2,2,4,3,4,3,2,1,4,1,2,2,4],[3,1,4,2,3,2,1,3,2,2,1,2,1,1,4,4,2,2,1,3,3,4,4,2,4,1,2,2,4,1,4,1,3],[3,3,4,3,4,1,1,2,1,3,2,4,2,3,1,2,4,3,4,2,1,2,3,4,1,4,1,1,2,2,3,2,2],[4,2,2,3,2,2,4,4,2,3,4,1,3,1,1,4,4,1,1,1,4,3,1,1,4,4,3,1,3,4,4,4,1],[2,1,2,4,1,2,1,2,2,3,4,3,4,1,2,1,1,4,4,3,2,4,3,3,4,2,1,4,4,1,2,1,4],[1,4,1,3,2,2,3,3,2,4,1,4,3,2,2,1,1,3,1,4,3,2,3,1,1,2,2,1,1,1,1,4,4],[4,1,2,3,2,1,3,4,4,2,1,2,2,1,1,4,3,3,1,4,3,1,4,3,2,3,4,1,4,4,2,1,3],[2,1,2,4,4,3,3,3,4,1,3,3,3,4,3,3,4,3,1,4,3,4,4,2,4,4,2,2,2,2,2,4,1],[1,4,2,2,4,1,2,3,2,4,3,3,2,1,2,3,1,4,2,1,1,2,4,3,2,3,1,2,4,4,1,4,3],[3,3,2,2,1,4,2,1,1,3,1,2,2,4,4,2,3,3,1,2,4,3,4,3,1,2,1,4,1,3,1,2,3],[2,1,4,3,1,3,2,4,4,4,4,1,3,1,1,1,2,2,2,3,1,1,4,1,2,1,2,2,4,3,3,1,4],[4,3,3,1,3,1,4,1,3,3,1,1,2,4,2,1,3,1,2,1,2,4,2,4,4,1,2,1,1,2,3,1,1],[1,2,2,1,3,1,2,3,4,4,1,3,1,2,1,3,2,1,4,1,4,1,4,2,1,2,1,1,2,3,2,1,4],[3,2,2,4,3,1,3,4,4,4,4,1,4,3,2,4,2,2,2,2,3,4,1,2,4,4,1,1,1,4,3,4,1],[2,3,4,1,4,3,4,1,1,3,3,1,2,2,1,3,4,1,2,4,2,1,4,2,4,3,3,1,1,1,2,2,4],[1,1,2,1,1,1,4,3,4,1,2,4,2,4,1,2,1,3,3,2,3,2,1,4,4,2,1,3,2,4,2,3,3],[4,4,2,1,3,1,3,1,2,1,3,4,4,2,4,4,2,4,2,2,4,4,1,4,1,3,2,2,2,2,1,2,2],[2,1,1,1,4,2,3,2,2,1,2,4,1,2,2,2,1,4,3,1,3,2,2,4,1,4,3,3,3,2,4,3,2],[2,2,4,2,1,2,1,2,1,3,4,1,4,4,2,4,2,1,4,2,1,3,3,3,3,2,2,3,1,3,1,4,4],[4,3,2,4,1,4,2,2,4,4,3,3,1,2,2,4,4,1,2,3,2,1,2,2,1,2,4,1,2,1,4,3,2],[4,1,3,2,2,4,1,3,2,2,1,4,2,1,2,3,3,1,2,1,4,1,3,1,4,3,2,1,4,4,4,4,1],[4,3,1,4,1,1,1,2,1,3,2,2,2,4,4,2,4,3,1,4,4,2,2,3,3,4,1,4,3,4,4,1,4],[2,4,3,3,3,4,2,4,2,4,3,3,1,1,1,4,4,3,4,3,2,3,4,1,3,4,2,1,2,3,2,1,3],[2,2,1,2,4,3,1,4,3,4,2,4,4,4,4,4,3,2,1,2,1,3,4,1,4,1,4,2,3,3,2,2,3],[3,4,2,1,1,2,1,3,3,2,1,3,3,2,3,2,2,4,4,2,2,1,2,2,1,4,1,2,1,2,3,4,2],[4,1,2,1,3,1,4,4,1,3,2,2,1,4,4,4,1,2,2,1,3,1,1,2,4,3,4,4,2,4,2,3,3],[1,3,1,2,2,1,1,2,4,1,3,3,4,4,3,1,2,4,1,4,1,3,2,4,2,1,1,3,1,3,4,3,3],[1,4,2,4,4,1,1,4,2,4,4,4,1,1,3,3,1,2,2,3,1,2,3,2,1,4,2,3,2,1,2,3,1],[4,1,2,2,3,1,2,4,1,3,2,4,2,3,1,3,3,2,3,1,3,2,1,4,4,1,4,2,2,1,3,1,2],[1,4,4,3,2,4,1,1,3,2,1,2,2,1,3,2,4,4,1,1,2,3,4,3,3,2,3,2,1,4,3,2,1],[2,3,2,4,4,3,1,3,4,2,1,3,4,3,2,4,2,3,2,4,4,4,4,4,3,4,2,2,3,3,2,3,2],[4,3,3,1,2,2,4,1,3,4,2,1,3,2,2,4,2,1,4,2,4,4,4,4,1,2,2,2,2,3,3,2,1],[2,2,4,1,3,4,3,2,1,4,2,2,3,1,1,2,4,3,2,2,1,1,4,2,1,1,2,2,2,2,4,4,1],[2,4,1,2,3,4,2,4,1,1,2,1,3,2,4,2,4,4,2,3,2,4,4,1,2,3,1,1,2,2,2,2,2],[3,4,1,1,2,4,2,3,4,4,3,2,4,4,4,4,1,4,3,4,1,2,3,1,1,2,4,4,4,3,1,3,2]]
    print(s.minCost(a)) # 36
