"""
https://leetcode.com/problems/the-maze-ii/?envType=study-plan&id=graph-ii

okay.. this should be easy I guess since I can reuse the logic from last problem
"""


from collections import deque
import heapq
from typing import List


class Solution:
    def shortestDistance(self, maze: List[List[int]], start: List[int], destination: List[int]) -> int:
        m, n = len(maze), len(maze[0])
        dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        def isWall(x, y):
            return not (0 <= x < m and 0 <= y < n) or maze[x][y] == 1

        bfsQ = deque()
        bfsQ.append((*start,0)) # x,y,steps
        # okay.. in scenarios like topo-sort, I need to separate one batch from another
        # especially when I need to count how many batches in total I need do a size countdown
        # but in typicall bfs traversal.. no need.. and here no need
        # but of course, you can do that as well... no big diff
        res = float('inf')
        while bfsQ:
            x, y, step = bfsQ.popleft()
            # this will signify the cell is processed
            maze[x][y] = 2

            if [x, y] == destination:
                res = min(res, step)
                continue

            for dx, dy in dirs:
                nX, nY, nStep = x, y, step
                while not isWall(nX+dx, nY+dy):
                    nX += dx
                    nY += dy
                    nStep += 1
                if maze[nX][nY] == 0:
                    # if it is already processed, ==2, don't add
                    bfsQ.append((nX, nY, nStep))
        return -1 if res == float('inf') else res

"""
69 / 78 test cases passed.

okay.. ok.. I probably should use heap to regulate the order
because the waling-to-a-wall could change the relative order

if using queue, I need to exhausteed all possibilities
huh.. still not right...

guess the avoid duplicate visit might be in the way
okay.. let me use the heap?
"""


class Solution:
    def shortestDistance(self, maze: List[List[int]], start: List[int], destination: List[int]) -> int:
        m, n = len(maze), len(maze[0])
        dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        def isWall(x, y):
            return not (0 <= x < m and 0 <= y < n) or maze[x][y] == 1

        bfsH = []
        heapq.heappush(bfsH, (0, *start))  # x,y,steps

        while bfsH:
            step, x, y = heapq.heappop(bfsH)
            # this will signify the cell is processed
            maze[x][y] = 2

            if [x, y] == destination:
                return step

            for dx, dy in dirs:
                nX, nY, nStep = x, y, step
                while not isWall(nX+dx, nY+dy):
                    nX += dx
                    nY += dy
                    nStep += 1
                if maze[nX][nY] == 0:
                    # if it is already processed, ==2, don't add
                    heapq.heappush(bfsH, (nStep, nX, nY))
        return -1

"""
huh.. still wrong....
ah.. heap is not right.. I use steps to sort but I didn't add it as the first element
fixed it quickly!

Runtime: 315 ms, faster than 76.73% of Python3 online submissions for The Maze II.
Memory Usage: 14.3 MB, less than 92.45% of Python3 online submissions for The Maze II.

thinking my naive dfs could solve this too?
"""


class Solution_recursive_hell:
    def shortestDistance(self, maze: List[List[int]], start: List[int], destination: List[int]) -> bool:
        m, n = len(maze), len(maze[0])
        dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        def isWall(x, y):
            return not (0 <= x < m and 0 <= y < n) or maze[x][y] == 1

        processed = {}
        def dfs(x, y, dx, dy):

            # rules:
            # 1. if x+dx,y+dy is a wall.. gives it a chance to change direction
            # 2. otherwise, it has to continue
            if [x, y] == destination and isWall(x+dx, y+dy):
                return 0

            if (x, y, dx, dy) in processed:
                return float('inf')

            if (x,y,dx,dy) in processed:
                return processed[x, y, dx, dy]

            res = float('inf')
            if isWall(x+dx, y+dy):
                for ndx, ndy in dirs:
                    if isWall(x+ndx, y+ndy) or (ndx==-dx and ndy ==-dy):
                        continue
                    res = min(res, dfs(x+ndx, y+ndy, ndx, ndy))
            else:
                res = dfs(x+dx, y+dy, dx, dy)

            processed[x, y, dx, dy] = res
            return res+1

        x, y = start
        res = float('inf')
        for dx, dy in dirs:
            if isWall(x+dx, y+dy):
                continue
            res = min(res, dfs(x, y, dx, dy))
        return -1 if res == float('inf') else res


"""
kay.. this is recursive hell
pingpong... no looking back?

        if isWall(x+ndx, y+ndy) or (ndx==-dy and ndy ==-dy):
            continue

okay.. even this won't prevent endless loop (not pingpong, but will become a dead loop)

let me see that dfs
need to introduce the path to maintain no repeating cells on a single path... (had forgotten that)
"""



class Solution_wrong_wrong_wrong:
    def shortestDistance(self, maze: List[List[int]], start: List[int], destination: List[int]) -> bool:
        m, n = len(maze), len(maze[0])
        dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        def isWall(x, y):
            return not (0 <= x < m and 0 <= y < n) or maze[x][y] == 1

        processed = {}
        def dfs(x, y, dx, dy, path):

            # rules:
            # 1. if x+dx,y+dy is a wall.. gives it a chance to change direction
            # 2. otherwise, it has to continue
            if [x, y] == destination and isWall(x+dx, y+dy):
                return 0

            if (x, y, dx, dy) in path:
                return float('inf')

            if (x, y, dx, dy) in processed:
                return processed[x, y, dx, dy]

            res = float('inf')
            if isWall(x+dx, y+dy):
                for ndx, ndy in dirs:
                    if isWall(x+ndx, y+ndy):
                        continue
                    res = min(res, dfs(x+ndx, y+ndy, ndx, ndy, path.union({(x,y,dx,dy)})))
            else:
                res = dfs(x+dx, y+dy, dx, dy, path.union({(x, y, dx, dy)}))

            processed[x, y, dx, dy] = res
            return res+1

        x, y = start
        res = float('inf')
        for dx, dy in dirs:
            if isWall(x+dx, y+dy):
                continue
            res = min(res, dfs(x, y, dx, dy, set()))
        return -1 if res == float('inf') else res


class Solution_dfs_but_wrong:
    def shortestDistance(self, maze: List[List[int]], start: List[int], destination: List[int]) -> bool:
        m, n = len(maze), len(maze[0])
        dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        def isWall(x, y):
            return not (0 <= x < m and 0 <= y < n) or maze[x][y] == 1

        processed = {}
        def dfs(x, y, path):
            # rules:
            # 1. if x+dx,y+dy is a wall.. gives it a chance to change direction
            # 2. otherwise, it has to continue -
            #   for it to continue, I don't need to add the middle cells to process
            #   only need to deal with the cells that can change directions
            if (x, y) in processed:
                # just return False, it will not change results
                return processed[x, y]

            if (x, y) in path:
                return float('inf')

            if [x, y] == destination:
                return 0

            res = float('inf')
            for dx, dy in dirs:
                nX, nY, l = x, y, 0
                while not isWall(nX+dx, nY+dy):
                    nX += dx
                    nY += dy
                    l += 1
                
                res = min(res, dfs(nX, nY, path.union({(x,y)})) + l)
            
            processed[x,y] = res
            return res
        res = dfs(*start, set())
        if res == float('inf'):
            return -1
        return res

"""
wrong!!

okay.. so a graph, the way points is 
    - the start
    - the end (if it is adjacent to a wall and an open cell on the same row or column)
    - the cells adjacent to a wall reachable from last position
    - the steps is the weight
    - calculate the shortest path
    - why dfs cannot work for me (heap dijstra is naturally here)
"""


class Solution_ugly_and_wrong:
    def shortestDistance(self, maze: List[List[int]], start: List[int], destination: List[int]) -> int:
        m, n = len(maze), len(maze[0])

        def isWall(x, y):
            return not (0 <= x < m and 0 <= y < n) or maze[x][y] == 1

        desX, desY = destination
        bfsQ = deque()
        if isWall(desX-1, desY) ^ isWall(desX+1, desY):
            # one adjacent wall vertical.. true
            # two adjacent walls vertical.. cannot reach it by vertical
            # -1: horizal reachable; 1 vertical reachable
            bfsQ.append((desX, desY, 1,0))
        if isWall(desX, desY-1) ^ isWall(desX, desY+1):
            # -1: horizal reachable; 1 vertical reachable
            bfsQ.append((desX, desY, -1,0))

        processed = set()

        while bfsQ:
            sz = len(bfsQ)
            while sz:
                x, y, dir, steps = bfsQ.popleft()
                if (x, y, dir) in processed:
                    sz -= 1
                    continue
                if [x, y] == start:
                    return steps
                processed.add((x, y, dir))

                # if left is wall, all the right cells up to next wall is equivilent to this cell
                # ditto for other 3 directions
    
                if dir == 1:
                    # this cell can reach dest vertically
                    # then on the same column between same two walls, it also reach the dest vertically
                    if isWall(x-1, y):
                        x1 = x
                        steps2 = steps+1
                        while not isWall(x1+1, y) and (x1+1, y, dir) not in processed:
                            bfsQ.append((x1+1, y, dir, steps2))
                            x1 += 1
                            steps2+=1
                    if isWall(x+1, y):
                        x2 = x
                        steps2 = steps+1
                        while not isWall(x2-1, y) and (x2-1, y, dir) not in processed:
                            bfsQ.append((x2-1, y, dir, steps2))
                            x2 -= 1
                            steps2+=1

                    # there is also this change direction logic here
                    if isWall(x, y-1) and not isWall(x, y+1):
                        # cell x,y can reach vertical and left is wall, means on this row, between two same walls
                        # it can reach dest
                        y1 = y
                        steps2 = steps
                        while not isWall(x, y1) and (x, y1, -dir) not in processed:
                            bfsQ.append((x, y1, -dir, steps2))
                            y1 += 1
                            steps2+=1
                    if isWall(x, y+1) and not isWall(x, y-1):
                        y2 = y
                        steps2 = steps
                        while not isWall(x, y2) and (x, y2, -dir) not in processed:
                            bfsQ.append((x, y2, -dir, steps2))
                            y2 -= 1
                            steps2+=1
                else:
                    if isWall(x, y-1):
                        y1 = y
                        steps2 = steps+1
                        while not isWall(x, y1+1) and (x, y1+1, dir) not in processed:
                            bfsQ.append((x, y1+1, dir, steps2))
                            y1 += 1
                            steps2+=1
                    if isWall(x, y+1):
                        y2 = y
                        steps2 = steps+1
                        while not isWall(x, y2-1) and (x, y2-1, dir) not in processed:
                            bfsQ.append((x, y2-1, dir, steps2))
                            y2 -= 1
                            steps2+=1

                    # ditto: above is adding equivilent cells
                    # below is adding changing direction cells
                    if isWall(x-1, y) and not isWall(x+1, y):
                        x1 = x
                        steps2 =  steps
                        while not isWall(x1, y) and (x1, y, -dir) not in processed:
                            bfsQ.append((x1, y, -dir, steps2))
                            x1 += 1
                    if isWall(x+1, y) and not isWall(x-1, y):
                        x2 = x
                        steps2 = steps
                        while not isWall(x2, y) and (x2, y, -dir) not in processed:
                            bfsQ.append((x2, y, -dir, steps2))
                            x2 -= 1
                            steps2 += 1

                sz -= 1

        return -1

"""
okay... I only got right using heap(dijstra)
but this can be solved with plain bfs/dfs with some variance

my attempts all failed.. probably I missed some logic.
I see others maintain the dist so far.. basically like relax the edges 

trick for that is 
    record the dist so far from start, 
        for simplicity, start cell is recorded as 1 to simplfy testing again unvisited cells
        and just to minus 1 to get the final result
    bfs/dfs all the reachables..
        the start cell has cost, adding the middle cells for the dest cell's cost
        if it is not zero(meaning can be reached by another cell) and the value is actually smaller then this is not the optimal path

with this in mind, give a try
"""


class Solution:
    def shortestDistance(self, maze: List[List[int]], start: List[int], destination: List[int]) -> int:
        m, n = len(maze), len(maze[0])
        dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        def isWall(x, y):
            return not (0 <= x < m and 0 <= y < n) or maze[x][y] == 1

        q = deque()
        maze[start[0]][start[1]] = 2
        q.append(start)
        while q:
            x,y = q.popleft()

            for dx,dy in dirs:
                nx,ny,cost = x,y,maze[x][y]
                while not isWall(nx+dx,ny+dy):
                    nx += dx
                    ny += dy
                    cost += 1
                if 0 < maze[nx][ny] <= cost:
                    continue
                maze[nx][ny] = cost 
                q.append([nx,ny])
        
        # intresting, this happens also to deal with non-reachable case
        # in which case, the destination will be 0, 0-1 will be -1...
        res = maze[destination[0]][destination[1]]-2
        if res == -2:
            return -1
        return res

"""
Runtime: 333 ms, faster than 70.00% of Python3 online submissions for The Maze II.
Memory Usage: 14.4 MB, less than 88.16% of Python3 online submissions for The Maze II.


okay.. the tricky part is 1 means wall so the start cell should start with 2 (not 1)
or any postive number other than 1..

yeah.. this is ... 
try dfs
"""


class Solution:
    def shortestDistance(self, maze: List[List[int]], start: List[int], destination: List[int]) -> int:
        m, n = len(maze), len(maze[0])
        dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        def isWall(x, y):
            return not (0 <= x < m and 0 <= y < n) or maze[x][y] == 1

        maze[start[0]][start[1]] = 2

        def dfs(x,y):
            if [x,y] == destination:
                return

            for dx,dy in dirs:
                nx,ny,cost = x,y,maze[x][y]
                while not isWall(nx+dx,ny+dy):
                    nx += dx
                    ny += dy
                    cost += 1
                if 0 < maze[nx][ny] <= cost:
                    continue
                maze[nx][ny] = cost 
                dfs(nx,ny)
        
        dfs(*start)
        res = maze[destination[0]][destination[1]]-2
        if res == -2:
            return -1
        return res

"""
37 / 78 test cases passed.
TLE...

huh.. okay.. this problem exposes so many blind spots 

okay.. this is not very smart dfs.. 
no cache can be used in this case.. because at each wall this can go to 2 directions, 2^n

this is dfs + dp.. but cannot use cache.. so TLE

bfs is still better.. either dijstra or plain bfs (with edge relaxing strategy)

thinking can I apple the edge-relaxing-order to cell-by-cell dfs or bfs?
but how to tell if a cell should stop? because when dest is a through cell.. it is not stoppable 
    with a wall to some side.. but that is not right...
    if I put in dx,dy.. hmm... so nah.. that makes things too complicateed

okay.. this thought train is suspended 

"""

if __name__ == '__main__':
    s = Solution()
    print(s.shortestDistance(maze=[[0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [
          1, 1, 0, 1, 1], [0, 0, 0, 0, 0]], start=[0, 4], destination=[4, 4]))
    print(s.shortestDistance(maze=[[0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [
          1, 1, 0, 1, 1], [0, 0, 0, 0, 0]], start=[0, 4], destination=[3, 2]))

    print(s.shortestDistance(maze=[[0, 0, 0, 0, 0], [1, 1, 0, 0, 1], [0, 0, 0, 0, 0], [
          0, 1, 0, 0, 1], [0, 1, 0, 0, 0]], start=[4, 3], destination=[0, 1]))

    print(s.shortestDistance(maze=[[0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [1, 1, 0, 1, 1], [0, 0, 0, 0, 0]],
                    start=[0, 4], destination=[1, 2]))

