"""
https://leetcode.com/problems/the-maze-iii/?envType=study-plan&id=graph-ii

think BFS, record cost and the string?

"""


from collections import deque
from typing import List


class Solution:
    def findShortestWay(self, maze: List[List[int]], ball: List[int], hole: List[int]) -> str:
        m, n = len(maze), len(maze[0])
        dirs = [[1, 0, 'd'], [0, -1,'l'], [0, 1,'r'], [-1, 0,'u']] # d<l<r<u but no use

        path = [['z']*n for _ in range(m)]
        def isWallOrHole(x, y):
            return not (0 <= x < m and 0 <= y < n) or maze[x][y] == 1 or [x,y] == hole

        q = deque()
        maze[ball[0]][ball[1]] = 2
        path[ball[0]][ball[1]] = ""
        q.append((ball[0],ball[1])) # x,y

        minCost = float('inf')
        res = 'z'
        while q:
            x,y = q.popleft()

            print(x,y, maze[x][y], path[x][y])
            if [x,y] == hole:
                if maze[x][y] == minCost:
                    res = min(res, path[x][y])
                if maze[x][y] < minCost:
                    res = path[x][y]
                    minCost = maze[x][y]
                continue

            for dx,dy,ds in dirs:
                nx,ny,cost,pStr = x,y,maze[x][y], path[x][y]
                
                while not isWallOrHole(nx+dx,ny+dy):
                    nx += dx
                    ny += dy
                    cost += 1
                
                if [nx+dx,ny+dy] == hole:
                    nx,ny = hole 
                    cost += 1
  
                if 0 < maze[nx][ny] < cost or (maze[nx][ny] == cost and pStr+ds > path[nx][ny]):
                    continue 
                maze[nx][ny] = cost
                path[nx][ny] = pStr+ds
                q.append((nx,ny))
        if res < 'z':
            return res
        return "impossible"


"""
Runtime: 77 ms, faster than 47.00% of Python3 online submissions for The Maze III.
Memory Usage: 14.1 MB, less than 26.00% of Python3 online submissions for The Maze III

I cannot go to ski this week
I feel pressure to warm up system design knowledges..
but I am really nearly crashing point... 

this problem is not that difficult.. only need to introduce another criteria 
however I struggle/tumble/stumble..

I am toasted...

okay.. since now only the most shortest and lexi smallest path can reach
so no need to compare.. 

just do this 
            if [x, y] == hole:
                res = path[x][y]
                continue

okay.. my energy level is low today..
maybe I'll come back another day to do dfs

and also maybe the heapq...
"""


class Solution:
    def findShortestWay(self, maze: List[List[int]], ball: List[int], hole: List[int]) -> str:
        m, n = len(maze), len(maze[0])
        dirs = [[1, 0, 'd'], [0, -1, 'l'], [0, 1, 'r'],
                [-1, 0, 'u']]  # d<l<r<u but no use

        path = [['z']*n for _ in range(m)]

        def isWallOrHole(x, y):
            return not (0 <= x < m and 0 <= y < n) or maze[x][y] == 1 or [x, y] == hole

        q = deque()
        maze[ball[0]][ball[1]] = 2
        path[ball[0]][ball[1]] = ""
        q.append((ball[0], ball[1]))  # x,y

        res = 'z'
        while q:
            x, y = q.popleft()

            # print(x,y, maze[x][y], path[x][y])
            if [x, y] == hole:
                res = path[x][y]
                continue

            for dx, dy, ds in dirs:
                nx, ny, cost, pStr = x, y, maze[x][y], path[x][y]

                while not isWallOrHole(nx+dx, ny+dy):
                    nx += dx
                    ny += dy
                    cost += 1

                if [nx+dx, ny+dy] == hole:
                    nx, ny = hole
                    cost += 1

                if 0 < maze[nx][ny] < cost or (maze[nx][ny] == cost and pStr+ds > path[nx][ny]):
                    continue
                maze[nx][ny] = cost
                path[nx][ny] = pStr+ds
                q.append((nx, ny))
        if res < 'z':
            return res
        return "impossible"




if __name__ == '__main__':
    s = Solution()
    # print(s.findShortestWay(maze=[[0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 1, 0], [
    #       0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1]], ball=[0, 4], hole=[3, 5]))
    print(s.findShortestWay( maze = [[0,0,0,0,0],[1,1,0,0,1],[0,0,0,0,0],[0,1,0,0,1],[0,1,0,0,0]], ball = [4,3], hole = [0,1]))

    maze=[[0,0,1,0,0],[0,0,0,0,0],[0,0,0,1,0],[1,1,0,1,1],[0,0,0,0,0]]
    ball = [0,4]
    hole = [4,4]

    print(s.findShortestWay(maze, ball, hole))
