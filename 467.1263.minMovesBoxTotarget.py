"""
https://leetcode.com/problems/minimum-moves-to-move-a-box-to-their-target-location/?envType=study-plan&id=graph-ii

interesting... 

it has two locations to consider: the box and the humnan

what allows to move a box to a direction 
    1. human must be able to reach the empty cell in the opposite direction 
        either by moving there
        or start from there
    2. of course, you can move to empty cell or target

so where can a human start?
    around the boxes.. the empty cells.. 

ah.. wait.. the T is treated as a passable cell.. human can pass it
so what I am thinking is

    union all the adjacent cells, S and T - that is where human can move.. 
    union all the adjacent cells with B.. if B can move to that location?

    hmm..

    why union find? 
        I am thinking if a box is adjacent to the target.. I can quickly tell if I can reach the opposite direction 

so what is the main mover?
    human or box??

following my union thoughts
    union all places I can be
    then look at the box.. 
        if it can move to one direction.. 
            move it.. (union its original position but box cell is blacked out.. 
            but will it block some other cells?, yes it will 
            so union find is not that viable here...
            pause this train here)

so I track two positions
    human pos
    box pos..

    the thing is to move box towards target
    and move human to the proper postion to push the box
    if both are reachable.. then yes
    otherwise, that path is not possible

very complicated.. 
but guess let me start some coding and see where it goes


"""


from collections import defaultdict, deque
from typing import List


class Solution:
    def minPushBox(self, grid: List[List[str]]) -> int:
        dirs = [[-1,0],[1,0],[0,1],[0,-1]]
        m,n = len(grid), len(grid[0])
        tX=tY=sX=sY=bX=bY=-1
        for x in range(m):
            for y in range(n):
                if grid[x][y] == 'T':
                    tX, tY = x,y
                if grid[x][y] == 'S':
                    sX,sY = x,y
                if grid[x][y] == 'B':
                    bX,bY= x,y

        def reachable(x1,y1,x2,y2, bx, by):
            if (bx,by) == (2,1):
                breaker = 1 
            q = deque()
            q.append((x1,y1))
            visited = set()
            while q:
                x,y = q.popleft()
                if (x,y) in visited:
                    continue
                visited.add((x,y))
                if (x,y) == (x2,y2):
                    return True
                for dx, dy in dirs:
                    nx,ny = x+dx,y+dy
                    if 0<=nx<m and 0<=ny<n and (grid[nx][ny] != '#' and (nx,ny)!=(bx,by)):
                        q.append((nx,ny))
            return False

        boxMoveQ = deque()
        boxMoveQ.append((bX, bY, sX, sY, 0)) # box loc, start loc, cost so far
        visited = set()
        while boxMoveQ:
            bX,bY,sX, sY, cost = boxMoveQ.popleft()
            if (bX, bY) in visited:
                continue
            visited.add((bX, bY))
            if (bX, bY) == (tX, tY):
                return cost

            pushLocs = set() 
            for dx, dy in dirs:
                pushFromX, pushFromY = bX+dx,bY+dy
                pushToX, pushToY = bX-dx, bY-dy
                if 0 <= pushFromX < m and 0 <= pushFromY < n \
                        and 0 <= pushToX < m and 0 <= pushToY < n \
                    and grid[pushFromX][pushFromY] != '#' \
                        and grid[pushToX][pushToY] != '#':
                            # was doing following for some reason to make logic more clear
                            # but I forget 'S' so a foot gun for sure
                        # and grid[pushFromX][pushFromY] in '.BT' \
                        # and grid[pushToX][pushToY] in '.BT':
                    pushLocs.add((pushFromX, pushFromY, pushToX, pushToY, sX, sY))

            # check if pushFrom can be reached from S,
            # if yes, then add pushTo to boxMoveQ and record
            for pushFromX, pushFromY, pushToX, pushToY, sx, sy in pushLocs:
                # bfs - (sX, sY) to pushFrom
                if (pushToX, pushToY) not in visited and reachable(sx, sy, pushFromX, pushFromY, bX, bY):
                    # push.. 
                    boxMoveQ.append((pushToX, pushToY, bX, bY, cost+1))
            
        return -1


"""
okay.. 21/30 passed.. not too bad not too good..

[["#",".",".","#","T","#","#","#","#"],["#",".",".","#",".","#",".",".","#"],["#",".",".","#",".","#","B",".","#"],["#",".",".",".",".",".",".",".","#"],["#",".",".",".",".","#",".","S","#"],["#",".",".","#",".","#","#","#","#"]]

okay.. draw it and easy to see.. it has to revisited a position from reverse direction
so that visited has some problem
"""


class Solution:
    def minPushBox(self, grid: List[List[str]]) -> int:
        dirs = {'u':[-1, 0], 'd':[1, 0], 'r':[0, 1], 'l':[0, -1]}
        m, n = len(grid), len(grid[0])
        tX = tY = sX = sY = bX = bY = -1
        for x in range(m):
            for y in range(n):
                if grid[x][y] == 'T':
                    tX, tY = x, y
                if grid[x][y] == 'S':
                    sX, sY = x, y
                if grid[x][y] == 'B':
                    bX, bY = x, y

        def reachable(x1, y1, x2, y2, bx, by):
            q = deque()
            q.append((x1, y1))
            visited = set()
            while q:
                x, y = q.popleft()
                if (x, y) in visited:
                    continue
                visited.add((x, y))
                if (x, y) == (x2, y2):
                    return True
                for dx, dy in dirs.values():
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < m and 0 <= ny < n and (grid[nx][ny] != '#' and (nx, ny) != (bx, by)):
                        q.append((nx, ny))
            return False

        boxMoveQ = deque()
        boxMoveQ.append((bX, bY, sX, sY, 0, ""))  # box loc, start loc, cost so far, direction
        visited = set()
        while boxMoveQ:
            bX, bY, sX, sY, cost, dir = boxMoveQ.popleft()
            if (bX, bY, dir) in visited:
                continue
            visited.add((bX, bY, dir))
            if (bX, bY) == (tX, tY):
                return cost

            pushLocs = set()
            for dir, (dx, dy) in dirs.items():
                pushFromX, pushFromY = bX+dx, bY+dy
                pushToX, pushToY = bX-dx, bY-dy
                if 0 <= pushFromX < m and 0 <= pushFromY < n \
                        and 0 <= pushToX < m and 0 <= pushToY < n \
                        and grid[pushFromX][pushFromY] != '#' \
                        and grid[pushToX][pushToY] != '#':
                    pushLocs.add(
                        (pushFromX, pushFromY, pushToX, pushToY, sX, sY, dir))

            # check if pushFrom can be reached from S,
            # if yes, then add pushTo to boxMoveQ and record
            for pushFromX, pushFromY, pushToX, pushToY, sx, sy, dir in pushLocs:
                # bfs - (sX, sY) to pushFrom
                if (pushToX, pushToY) not in visited and reachable(sx, sy, pushFromX, pushFromY, bX, bY):
                    # push..
                    boxMoveQ.append((pushToX, pushToY, bX, bY, cost+1, dir))

        return -1

"""
ugh.. really struggling

wrong here
[["#",".",".",".",".",".",".",".",".","."],[".",".",".",".",".","#",".",".",".","#"],["#",".","#",".",".","T",".",".",".","."],[".","#",".",".",".",".",".",".",".","."],[".",".",".",".",".",".","#",".",".","."],[".",".",".","#","#","S",".","B",".","."],["#",".",".",".",".",".",".","#",".","."],[".","#",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".",".","."],[".",".",".",".",".","#",".",".",".","."]]


# . . . . . . . . .
. . . . . # . . . #
# . # . . T . . . .
. # . . . . . . . .
. . . . . . # . . .
. . . # # S . B . .
# . . . . . . # . .
. # . . . . . . . .
. . . . . . . . . .
. . . . . # . . . .

easy to see this is 5
why I got 7?

oh maybe I ignored S can be B position??

okay.. finally
Runtime: 253 ms, faster than 61.09% of Python3 online submissions for Minimum Moves to Move a Box to Their Target Location.
Memory Usage: 14.2 MB, less than 72.37% of Python3 online submissions for Minimum Moves to Move a Box to Their Target Location.
"""

if __name__ == '__main__':
    s = Solution()
    print(s.minPushBox(grid = 
            [["#","#","#","#","#","#"],
            ["#","T","#","#","#","#"],
            ["#",".",".","B",".","#"],
            ["#",".","#","#",".","#"],
            ["#",".",".",".","S","#"],
            ["#","#","#","#","#","#"]]))

    print(s.minPushBox(grid = [["#","#","#","#","#","#"],
               ["#","T","#","#","#","#"],
               ["#",".",".","B",".","#"],
               ["#","#","#","#",".","#"],
               ["#",".",".",".","S","#"],
               ["#","#","#","#","#","#"]]))

    
    print(s.minPushBox(grid = [["#","#","#","#","#","#"],
               ["#","T",".",".","#","#"],
               ["#",".","#","B",".","#"],
               ["#",".",".",".",".","#"],
               ["#",".",".",".","S","#"],
               ["#","#","#","#","#","#"]]))
    
    grid = [["#",".",".","#","T","#","#","#","#"],["#",".",".","#",".","#",".",".","#"],["#",".",".","#",".","#","B",".","#"],["#",".",".",".",".",".",".",".","#"],["#",".",".",".",".","#",".","S","#"],["#",".",".","#",".","#","#","#","#"]]
    print(s.minPushBox(grid))

    grid = [["#",".",".",".",".",".",".",".",".","."],[".",".",".",".",".","#",".",".",".","#"],["#",".","#",".",".","T",".",".",".","."],[".","#",".",".",".",".",".",".",".","."],[".",".",".",".",".",".","#",".",".","."],[".",".",".","#","#","S",".","B",".","."],["#",".",".",".",".",".",".","#",".","."],[".","#",".",".",".",".",".",".",".","."],[".",".",".",".",".",".",".",".",".","."],[".",".",".",".",".","#",".",".",".","."]]
    print(s.minPushBox(grid))
