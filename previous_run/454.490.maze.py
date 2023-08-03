"""
https://leetcode.com/problems/the-maze/?envType=study-plan&id=graph-ii

took me a while to understand the question correctly
so 
    - balls must hit a wall before changing directions
        that means.. if it moves left.. it need to move to a wall before it can change directions
    - on the opposite direction of the incoming ball, there must be a wall behind the destination to stop the ball
        other it rolls through

okay... so sounds like 
    we can scan from 4 directions (in 2 loops maybe)
    get the upper/lower/left/right wall location 

or maybe just dfs search?
"""


from collections import deque
from typing import List


class Solution:
    def hasPath(self, maze: List[List[int]], start: List[int], destination: List[int]) -> bool:
        m, n = len(maze), len(maze[0])
        dirs = [[-1,0],[1,0],[0,-1],[0,1]]

        def isWall(x,y):
            return not (0<=x<m and 0<=y<n) or maze[x][y] == 1

        def dfs(x,y,dx,dy):

            # rules:
            # 1. if x+dx,y+dy is a wall.. gives it a chance to change direction 
            # 2. otherwise, it has to continue
            if [x,y] ==  destination and isWall(x+dx,y+dy):
                return True
            
            # avoid the ping pong effect as well
            maze[x][y] = 2

            if isWall(x+dx, y+dy):
                for ndx,ndy in dirs:
                    if isWall(x+ndx, y+ndy):
                        continue
                    if maze[x+ndx][y+ndy] == 0 and dfs(x+ndx,y+ndy,ndx,ndy):
                        return True
            else:
                return dfs(x+dx,y+dy,dx,dy)

            return False

        x,y = start
        for dx,dy in dirs:
            if isWall(x+dx, y+dy):
                continue
            if dfs(x,y,dx,dy):
                return True
        return False
    
"""
failed at

[[0,0,1,0,0],[0,0,0,0,0],[0,0,0,1,0],[1,1,0,1,1],[0,0,0,0,0]]
[0,4]
[1,2]

okay that avoid pingpong is not right..
just give it a parent maybe

or maybe abs(dx,dy) = abs(dx,dy) something
huh.. it must be able to go back to parent node.. other above example won't work

okay.. time to work out a bit..
leave this to afternoon... after interview 


"""

"""
okay... after interview and vaccine shot
I entered a dreadful side-effect time

now I am recovered after 1 full day I can think again

so search from start to destination is not easy
    - if I don't deal with repeating steps... I could end up recursion hell
    - if I do that, I miss some scenarios that must be sovled by walk the cell recursively
        - wait.. actually.. that is not really repeating - the direction is different
        - hold this thought and come visit it again later

so I am think, maybe I can start from the destination 
    - if the left/right is a wall.. then I could say, between this wall and another wall it can reach
        all the cells can reach destination ... 
        I could save up (x,y,+/-1,0) to mean that
    - then I think, this can be simplifed 
        to (x,y, H or V)
    - then I think, this can be furthure simplifed 
        to  Vertical (x,y)   (not the full row.. because of the wall placement)
        and Horizontal (x,y)
        I might be able do do BFS here..
            expand the reachable cells from the destination cell 
            pop the queue, 
                if left/right is cell.. adding all the cells on the same row between two walls to queue
                if up/down is cell... adding all the cells on the same column between two walls to queue
            if the element is processed, skip..
            if the element is start, return true...



"""


class Solution:
    def hasPath(self, maze: List[List[int]], start: List[int], destination: List[int]) -> bool:
        m, n = len(maze), len(maze[0])

        bfsQ = deque()
        bfsQ.append(destination)

        while bfsQ:
            sz = len(bfsQ)
            while sz:
                x,y = bfsQ.popleft()

                if maze[x-1][y] == 1:
                    # up is wall: adding all cells between two walls to q
                    while x+1<m and maze[x+1][y]==0:
                        bfsQ.append
                        ...

"""
something came up while I am coding
mightbe I need two queues - vertical queue and horizon queue?
not really... hmm.. I need a state for that at least


"""


class Solution:
    def hasPath(self, maze: List[List[int]], start: List[int], destination: List[int]) -> bool:
        m, n = len(maze), len(maze[0])
        def isWall(x, y):
            return not (0<=x<m and 0<=y<n) or maze[x][y] == 1

        desX, desY = destination
        bfsQ = deque()
        if isWall(desX-1, desY) ^ isWall(desX+1, desY):
            # one adjacent wall vertical.. true
            # two adjacent walls vertical.. cannot reach it by vertical
            bfsQ.append((desX, desY, 1)) # -1: horizal reachable; 1 vertical reachable 
        if isWall(desX, desY-1) ^ isWall(desX, desY+1):
            # -1: horizal reachable; 1 vertical reachable
            bfsQ.append((desX, desY, -1))

        processed = set()
        while bfsQ:
            sz = len(bfsQ)
            while sz:
                x, y, dir = bfsQ.popleft()
                if (x,y,dir) in processed:
                    sz-=1
                    continue
                if [x,y] == start:
                    return True
                processed.add((x,y,dir))
                
                # if left is wall, all the right cells up to next wall is equivilent to this cell
                # ditto for other 3 directions
                if dir==1:
                    # this cell can reach dest vertically
                    # then on the same column between same two walls, it also reach the dest vertically
                    if isWall(x-1,y):    
                        x1 = x
                        while not isWall(x1+1,y) and (x1+1,y,dir) not in processed:
                            bfsQ.append((x1+1,y, dir))
                            x1+=1
                    if isWall(x+1,y):
                        x2 = x
                        while not isWall(x2-1, y) and (x2-1, y, dir) not in processed:
                            bfsQ.append((x2-1,y, dir))
                            x2-=1
                    
                    # there is also this change direction logic here
                    if isWall(x,y-1) and not isWall(x,y+1):
                        # cell x,y can reach vertical and left is wall, means on this row, between two same walls
                        # it can reach dest 
                        y1=y
                        while not isWall(x,y1) and (x,y1, -dir) not in processed:
                            bfsQ.append((x,y1,-dir))
                            y1+=1
                    if isWall(x,y+1) and not isWall(x,y-1) :
                        y2=y
                        while not isWall(x,y2) and (x,y2, -dir) not in processed:
                            bfsQ.append((x,y2,-dir))
                            y2-=1
                else :
                    if isWall(x,y-1):
                        y1=y 
                        while not isWall(x, y1+1) and (x, y1+1, dir) not in processed:
                            bfsQ.append((x,y1+1,dir))
                            y1+=1
                    if isWall(x,y+1):
                        y2=y
                        while not isWall(x, y2-1) and (x, y2-1, dir) not in processed:
                            bfsQ.append((x,y2-1,dir))
                            y2-=1

                    # ditto: above is adding equivilent cells
                    # below is adding changing direction cells
                    if isWall(x-1,y) and not isWall(x+1,y):
                        x1=x 
                        while not isWall(x1,y) and (x1,y,-dir) not in processed:
                            bfsQ.append((x1,y,-dir))
                            x1+=1
                    if isWall(x+1,y) and not isWall(x-1,y):
                        x2=x
                        while not isWall(x2,y) and (x2,y,-dir) not in processed:
                            bfsQ.append((x2, y, -dir))
                            x2-=1
                        
                sz-=1
        return False


"""
Runtime: 327 ms, faster than 53.78% of Python3 online submissions for The Maze.
Memory Usage: 15.5 MB, less than 39.70% of Python3 online submissions for The Maze.

okay.. very long ugly code that is..
now return to dfs.. while knowing the dir should be one state for the processed set
"""                
                    
class Solution:
    def hasPath(self, maze: List[List[int]], start: List[int], destination: List[int]) -> bool:
        m, n = len(maze), len(maze[0])
        dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        def isWall(x, y):
            return not (0 <= x < m and 0 <= y < n) or maze[x][y] == 1

        processed = set()

        def dfs(x, y, dx, dy):

            # rules:
            # 1. if x+dx,y+dy is a wall.. gives it a chance to change direction
            # 2. otherwise, it has to continue
            if [x, y] == destination and isWall(x+dx, y+dy):
                return True

            if (x,y,dx,dy) in processed:
                # just return False, it will not change results
                return False
            processed.add((x,y,dx,dy))

            if isWall(x+dx, y+dy):
                for ndx, ndy in dirs:
                    if isWall(x+ndx, y+ndy):
                        continue
                    if dfs(x+ndx, y+ndy, ndx, ndy):
                        return True
            else:
                return dfs(x+dx, y+dy, dx, dy)

            return False

        x, y = start
        for dx, dy in dirs:
            if isWall(x+dx, y+dy):
                continue
            if dfs(x, y, dx, dy):
                return True
        return False

"""
Runtime: 311 ms, faster than 58.74% of Python3 online submissions for The Maze.
Memory Usage: 22.8 MB, less than 5.04% of Python3 online submissions for The Maze.

ah.. I see people simplify it by going straight to the end of line..
same thing but simpler 
    then you don't need to worry about the directions because at the cells adjacent to walls can change directions
"""


class Solution:
    def hasPath(self, maze: List[List[int]], start: List[int], destination: List[int]) -> bool:
        m, n = len(maze), len(maze[0])
        dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        def isWall(x, y):
            return not (0 <= x < m and 0 <= y < n) or maze[x][y] == 1

        processed = set()
        def dfs(x, y):
            # rules:
            # 1. if x+dx,y+dy is a wall.. gives it a chance to change direction
            # 2. otherwise, it has to continue -
            #   for it to continue, I don't need to add the middle cells to process
            #   only need to deal with the cells that can change directions 
            if (x, y) in processed:
                # just return False, it will not change results
                return False
            processed.add((x, y))

            if [x, y] == destination:
                return True
            
            for dx,dy in dirs:
                nX,nY = x,y
                while not isWall(nX+dx, nY+dy):
                    nX+=dx
                    nY+=dy
                if dfs(nX,nY):
                    return True
            return False
        return dfs(*start)
                
"""
Runtime: 289 ms, faster than 74.44% of Python3 online submissions for The Maze.
Memory Usage: 16.2 MB, less than 30.37% of Python3 online submissions for The Maze.

this also works - because the x,y (except start) is guranteed to be a cell adjacent to a wall and it can stop on that direction

class Solution:
    def hasPath(self, maze: List[List[int]], start: List[int], destination: List[int]) -> bool:
        m, n = len(maze), len(maze[0])
        dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        def isWall(x, y):
            return not (0 <= x < m and 0 <= y < n) or maze[x][y] == 1

        processed = set()
        def dfs(x, y):
            if [x, y] == destination:
                return True

            if (x, y) in processed:
                # just return False, it will not change results
                return False
            processed.add((x, y))
            
            for dx,dy in dirs:
                nX,nY = x,y
                while not isWall(nX+dx, nY+dy):
                    nX+=dx
                    nY+=dy
                if dfs(nX,nY):
                    return True
            return False
        return dfs(*start)

Runtime: 279 ms, faster than 85.19% of Python3 online submissions for The Maze.
Memory Usage: 16.2 MB, less than 30.37% of Python3 online submissions for The Maze.

so it goes same with the BFS
haha.. I tried to deal with every cell and that over-complicates things
"""


class Solution:
    def hasPath(self, maze: List[List[int]], start: List[int], destination: List[int]) -> bool:
        m, n = len(maze), len(maze[0])
        dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        def isWall(x, y):
            return not (0 <= x < m and 0 <= y < n) or maze[x][y] == 1
        
        bfsQ = deque()
        bfsQ.append(start)
        # okay.. in scenarios like topo-sort, I need to separate one batch from another
        # especially when I need to count how many batches in total I need do a size countdown
        # but in typicall bfs traversal.. no need.. and here no need
        # but of course, you can do that as well... no big diff
        while bfsQ:
            x,y = bfsQ.popleft()
            # this will signify the cell is processed
            maze[x][y] = 2

            if [x,y] == destination:
                return True
            
            for dx,dy in dirs:
                nX,nY = x,y
                while not isWall(nX+dx, nY+dy):
                    nX+=dx
                    nY+=dy
                if maze[nX][nY] == 0:
                    # if it is already processed, ==2, don't add
                    bfsQ.append([nX, nY])
        return False

"""
Runtime: 623 ms, faster than 30.52% of Python3 online submissions for The Maze.
Memory Usage: 14.5 MB, less than 82.59% of Python3 online submissions for The Maze.

"""


if __name__ == '__main__':
    s = Solution()
    print(s.hasPath(maze=[[0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [
          1, 1, 0, 1, 1], [0, 0, 0, 0, 0]], start=[0, 4], destination=[4, 4]))
    print(s.hasPath(maze=[[0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [
          1, 1, 0, 1, 1], [0, 0, 0, 0, 0]], start=[0, 4], destination=[3, 2]))

    print(s.hasPath(maze=[[0, 0, 0, 0, 0], [1, 1, 0, 0, 1], [0, 0, 0, 0, 0], [
          0, 1, 0, 0, 1], [0, 1, 0, 0, 0]], start=[4, 3], destination=[0, 1]))

    print(s.hasPath(maze=[[0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [1, 1, 0, 1, 1], [0, 0, 0, 0, 0]],
                    start=[0, 4],destination=[1, 2]))
