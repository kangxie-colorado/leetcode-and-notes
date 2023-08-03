"""
https://leetcode.com/problems/shortest-distance-from-all-buildings/?envType=study-plan&id=graph-ii

I am thinking is 

union find all 0 and 1.. 
because 1 <= m, n <= 50

maybe able to do it

then check the groups.. 
    if not enough 1 connected.. then -1
    if all 1 connected, in the same group.. get all the distiance????

probably not gonna work 
but just have a quick try
"""


from collections import defaultdict, deque
from typing import List


class Solution:
    def shortestDistance(self, grid: List[List[int]]) -> int:
        
        roots = {}

        def find(x,y):
            roots.setdefault((x,y), (x,y))
            if roots[x,y] != (x,y):
                roots[x,y] = find(*roots[x,y])
            return roots[x,y]
        
        def union(x1,y1,x2,y2):
            roots[find(x1,y1)] = roots[find(x2,y2)]

        m,n = len(grid), len(grid[0])
        ones = 0
        for i in range(m):
            for j in range(n):
                union(i,j,i,j)
                if grid[i][j] == 1:
                    ones += 1

                if i > 0 and grid[i-1][j] in (0, 1) and grid[i][j] in (0, 1):
                    union(i,j,i-1,j)
                if j > 0 and grid[i][j-1] in (0, 1) and grid[i][j] in (0, 1):
                    union(i,j,i,j-1)

        grpSets = defaultdict(set)
        onesPerGrp = defaultdict(set)
        reachAll = False
        grpToBuild = None
        for x,y in roots:
            r = find(x,y)
            grpSets[r].add((x,y))
            if grid[x][y] == 1:
                onesPerGrp[r].add((x,y))
                if len(onesPerGrp[r]) == ones:
                    grpToBuild = r
                    reachAll= True
        
        if not reachAll:
            return -1
        
        res = float('inf')
        for x,y in grpSets[grpToBuild]:
            if grid[x][y] == 0:
                dist= 0
                for x1,y1 in onesPerGrp[grpToBuild]:
                    dist += abs(x1-x) + abs(y1-y)
                res = min(res, dist)
        
        return res if res != float('inf') else -1

"""
[[1,1],[0,1]]

okay.. failed here.

let me adjust the algorithm 
only union the 0s.. but add adjacent ones to a set

also use a different map to track adjacent ones per root
"""


class Solution:
    def shortestDistance(self, grid: List[List[int]]) -> int:
        dirs = [(-1,0), (1,0), (0,1), (0,-1)]

        roots = {}
        adjacentOnes = defaultdict(set)
        def find(x, y):
            roots.setdefault((x, y), (x, y))
            if roots[x, y] != (x, y):
                roots[x, y] = find(*roots[x, y])
            return roots[x, y]

        def union(x1, y1, x2, y2):
            r1 = find(x1, y1)
            r2 = find(x2, y2)

            allOnes = adjacentOnes[r1].union(adjacentOnes[r2])
            adjacentOnes[r1] = adjacentOnes[r2] = allOnes
            roots[r1] = roots[r2]

        m, n = len(grid), len(grid[0])
        ones = 0
        for i in range(m):
            for j in range(n):
                union(i, j, i, j)
                if grid[i][j] == 2:
                    continue

                if grid[i][j] == 1:
                    ones += 1
                    continue
            
                for dx, dy in dirs:
                    x, y = i+dx, j+dy
                    if 0 <= x < m and 0 <= y < n and grid[x][y] == 1:
                        adjacentOnes[i, j].add((x, y))

                if i > 0 and grid[i-1][j] == grid[i][j] == 0:
                    union(i, j, i-1, j)
                if j > 0 and grid[i][j-1] == grid[i][j] == 0:
                    union(i, j, i, j-1)
                
        grpSets = defaultdict(set)
        grpToBuild = None
        for x, y in roots:
            if grid[x][y] == 0:
                r = find(x, y)
                grpSets[r].add((x, y))
                
                if len(adjacentOnes[r]) == ones:
                    grpToBuild = r
        
        if not grpToBuild:
            return -1
        
        res = float('inf')
        for x, y in grpSets[grpToBuild]:
            dist = 0
            for x1, y1 in adjacentOnes[grpToBuild]:
                dist += abs(x1-x) + abs(y1-y)
            res = min(res, dist)

        return res if res != float('inf') else -1


"""
ah.. if the direct route has to pass a house or an obstacle.. it cannot go thru
so my thinking is over simple.

I guess let's just do bfs

for fun, I keep my union find code although I think not that necessary
actuall no start a fresh one
"""
                

class Solution:
    def shortestDistance(self, grid: List[List[int]]) -> int:
        dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
                
        m, n = len(grid), len(grid[0])
        ones = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    ones += 1

        minDist = float('inf')
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 0:
                    # just run bfs 
                    q = deque()
                    q.append((i,j,0)) # x,y,dist
                    visisted = set()
                    reachOnes = defaultdict(int)

                    while q:
                        x,y,d = q.popleft()

                        if (x,y) in visisted:
                            continue
                        visisted.add((x,y))

                        for dx, dy in dirs:
                            x1, y1 = x+dx, y+dy
                            if 0 <= x1 < m and 0 <= y1 < n and grid[x1][y1] == 1:
                                if (x1,y1) not in reachOnes or d+1<reachOnes[x1,y1]:
                                    reachOnes[x1, y1] = d+1
                        
                            if 0 <= x1 < m and 0 <= y1 < n and grid[x1][y1] == 0:
                                q.append((x1,y1,d+1))
                    
                    if len(reachOnes) == ones:
                        dist = 0
                        for d in reachOnes.values():
                            dist += d
                        minDist = min(dist, minDist)
        return minDist if minDist != float('inf') else -1


"""
77 / 85 test cases passed.

okay.. let me add some early termination
    1, if d>minDist, no need to continue
    2. if x1,y1 is a cell that is known to be unreachable.. no need to continue
"""


class Solution:
    def shortestDistance(self, grid: List[List[int]]) -> int:
        dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        m, n = len(grid), len(grid[0])
        ones = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    ones += 1

        minDist = float('inf')
        unreachableCells = set()
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 0:
                    # just run bfs
                    q = deque()
                    q.append((i, j, 0))  # x,y,dist
                    visisted = set()
                    reachOnes = defaultdict(int)

                    while q:
                        x, y, d = q.popleft()

                        if (x, y) in visisted:
                            continue
                        visisted.add((x, y))

                        if (x,y) in unreachableCells:
                            unreachableCells.add((i, j))
                            break
                        
                        if d>=minDist:
                            # will not get better results
                            break 

                        for dx, dy in dirs:
                            x1, y1 = x+dx, y+dy
                            if 0 <= x1 < m and 0 <= y1 < n and grid[x1][y1] == 1:
                                if (x1, y1) not in reachOnes or d+1 < reachOnes[x1, y1]:
                                    reachOnes[x1, y1] = d+1

                            if 0 <= x1 < m and 0 <= y1 < n and grid[x1][y1] == 0:
                                q.append((x1, y1, d+1))

                    if len(reachOnes) == ones:
                        dist = 0
                        for d in reachOnes.values():
                            dist += d
                        minDist = min(dist, minDist)
                    else:
                        unreachableCells.add((i,j))
        return minDist if minDist != float('inf') else -1

"""
okay.. stil not fast enough
result is correct but TLE all the way

so this is the place to think now.

hmm... usually the x,y in the mid of 1s are better
we can start there and use early termination?

we can use union find to find out
"""


class Solution:
    def shortestDistance(self, grid: List[List[int]]) -> int:
        dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        roots = {}
        adjacentOnes = defaultdict(set)

        def find(x, y):
            roots.setdefault((x, y), (x, y))
            if roots[x, y] != (x, y):
                roots[x, y] = find(*roots[x, y])
            return roots[x, y]

        def union(x1, y1, x2, y2):
            r1 = find(x1, y1)
            r2 = find(x2, y2)

            allOnes = adjacentOnes[r1].union(adjacentOnes[r2])
            adjacentOnes[r1] = adjacentOnes[r2] = allOnes
            roots[r1] = roots[r2]

        m, n = len(grid), len(grid[0])
        ones = 0
        for i in range(m):
            for j in range(n):
                union(i, j, i, j)
                if grid[i][j] == 2:
                    continue

                if grid[i][j] == 1:
                    ones += 1
                    continue

                for dx, dy in dirs:
                    x, y = i+dx, j+dy
                    if 0 <= x < m and 0 <= y < n and grid[x][y] == 1:
                        adjacentOnes[i, j].add((x, y))

                if i > 0 and grid[i-1][j] == grid[i][j] == 0:
                    union(i, j, i-1, j)
                if j > 0 and grid[i][j-1] == grid[i][j] == 0:
                    union(i, j, i, j-1)

        grpSets = defaultdict(set)
        grpToBuild = None
        for x, y in roots:
            if grid[x][y] == 0:
                r = find(x, y)
                grpSets[r].add((x, y))

                if len(adjacentOnes[r]) == ones:
                    grpToBuild = r
        if not grpToBuild:
            return -1

        straightDist = defaultdict(int)
        for i, j in grpSets[grpToBuild]:
            dist = 0
            for x,y in adjacentOnes[grpToBuild]:
                dist += abs(x-i) + abs(y-j)
            straightDist[i,j] = dist

        minDist = float('inf')
        for i, j in sorted(grpSets[grpToBuild], key=lambda x: (abs(x[0]-m//2), abs(x[1]-n//2))):
            dist = 0
            q = deque()
            q.append((i, j, 0))  # x,y,dist
            visisted = set()
            reachOnes = defaultdict(int)

            if straightDist[i,j] >= minDist:
                continue

            while q:
                x, y, d = q.popleft()

                if (x, y) in visisted:
                    continue
                visisted.add((x, y))
                
                if d>=minDist:
                    # will not get better results
                    break 

                for dx, dy in dirs:
                    x1, y1 = x+dx, y+dy
                    if 0 <= x1 < m and 0 <= y1 < n and grid[x1][y1] == 1:
                        if (x1, y1) not in reachOnes or d+1 < reachOnes[x1, y1]:
                            reachOnes[x1, y1] = d+1

                    if 0 <= x1 < m and 0 <= y1 < n and grid[x1][y1] == 0:
                        q.append((x1, y1, d+1))

            dist = 0
            for d in reachOnes.values():
                dist += d
            minDist = min(dist, minDist)

        return minDist if minDist != float('inf') else -1


"""
I have no idea how to make this go faster
maybe one more optimization

if the straight (without concerning the house/obstale) dist is >= minDist.. then I also skip
hahahaha

Runtime: 2128 ms, faster than 95.87% of Python3 online submissions for Shortest Distance from All Buildings.
Memory Usage: 40.6 MB, less than 5.07% of Python3 online submissions for Shortest Distance from All Buildings.

I used pruning.. this and that technique to prun.. 
I'll revisit others' posts to learn some more
"""

if __name__ == '__main__':
    s = Solution()
    print(s.shortestDistance(
        grid=[[1, 0, 2, 0, 1], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [1, 0, 2, 0, 1], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0]]))
        
    grid =  [[0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,2,1,0,0,2,0,0,0,0,0,1,2,0,0,0,0,0,1,2,0,0,0,0,0,0,0,0,1,0,0,2,1,2,0,0],[0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,2,1,0,2,0,0,2,0,0,0,1,1,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,2,2,0,0,1,2,1,0,0,0,0,0,2,0,2,1,0,0,0,0,0,0,0],[0,1,0,0,1,0,0,0,0,0,0,0,2,0,0,2,0,0,0,0,0,0,1,0,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0,0,1,0,0,0,2,0,2,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,2,1,0],[2,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],[1,0,2,0,0,1,0,0,2,0,0,1,0,0,0,1,0,0,0,2,0,2,0,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,1,0,0,2,0,0],[0,2,0,1,0,0,0,1,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],[0,0,0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,0,1,0,0,0,0,2,0,0,0,0,0,1,0,0,0,0,0,0,0,0,2,0,1,0,0,0,0,0,0,0,0,0],[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,2,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,2,0,0,0,0,0],[0,0,0,2,0,0,0,2,0,1,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,2,0,2,0,0,1,0,0,0,1,2,0,0,0,0,0,0,1],[1,0,0,0,0,1,1,2,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,1,0,0,0,0,0,2,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,2,2,0,0,0,0,2,0,1,1,0,0],[0,2,0,0,0,1,1,0,0,0,2,0,0,0,0,0,0,0,0,1,0,1,0,0,0,2,1,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0],[0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,1,0,0,0,0,0,0,0,0,1,0,0,0,2,0,0,1,2,0,0,0,2,0,0,1],[0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,2],[0,2,0,2,0,2,0,0,0,0,0,0,0,0,1,2,0,0,0,0,0,0,1,0,1,0,0,2,0,0,1,0,1,0,0,0,0,0,0,0,1,0,2,0,0,0,0,0,0,1],[0,0,0,0,1,0,0,1,0,0,1,2,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2,0,0,0,1,0,2,0,0,0,0,0,1,2,2,0,0,0,0],[0,0,2,0,0,0,0,0,0,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,2],[0,0,1,0,0,0,1,0,2,0,0,0,0,0,0,0,0,0,0,2,0,1,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,2,0,0,0,0,2,0,0,0,0,0,0],[0,0,0,0,1,2,0,0,0,0,0,1,2,0,0,0,2,0,1,0,0,2,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0],[0,2,0,1,0,0,0,2,2,2,0,0,0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,2,0,1,0,0,0,0,0,2,0,1,2,0,0,0,0,0,0,2,0,0,0,0,2,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],[2,0,0,0,2,1,2,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,1,0,0,0,0,0],[0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,2,0,2,0,2,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,1],[0,2,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,1,2,0,0,0,0,0,1,0,0,0,0,0,0,0,2,0,0],[0,0,2,0,0,1,1,0,0,0,0,0,0,0,0,0,0,2,0,1,0,0,2,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,2],[1,0,0,2,1,0,0,0,0,0,0,0,2,1,0,0,0,0,0,2,0,0,0,0,2,0,0,0,0,0,1,0,0,0,0,2,0,0,0,0,0,1,0,1,0,0,0,0,0,2],[2,0,0,0,1,0,0,0,2,0,0,0,2,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0,1,0,0,2,0,1,0,0,1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,2,1,0,2,0,0,0,0,0,1,2,0,0,1,0],[1,0,0,0,0,0,0,0,2,0,2,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,2,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,2,2,0,0,0,0],[0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,2,0,0,0,0,0,0,0,0,0,0,2,0,0,2,0,0,0,2,0,0,0,1,0,0,2,0,1,2],[0,2,0,0,0,0,0,0,0,0,1,0,0,0,0,0,2,0,1,0,0,0,0,0,2,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,2,1,0,0,0],[0,0,0,0,0,0,0,0,2,0,0,0,0,0,1,0,0,0,0,0,0,2,1,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0],[0,1,0,0,0,0,0,0,2,1,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,2,2,0,0,0,0,0,1,0,0,0,0],[0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,2,1,1,0,0,1,0,0,0,0,0,0,0,0,2,0,2,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0],[0,0,1,0,1,0,0,0,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,2,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0],[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,1,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1,0,0],[0,0,0,0,2,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1,0,1,2,0,0,0,0,0,0,0,0,0,0,0,1],[0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,2,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,2,0,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,2,1,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0,0,0],[0,0,1,0,0,0,2,2,0,2,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],[0,0,2,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,2,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0],[0,0,0,0,0,1,0,0,0,0,0,1,1,2,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,2,0,0,2,0,0,0,2,0,0,0,0,0,2,0,2,0,0],[0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,2,0,0,1,0,0,2,2,0,0,2,0,0,0,1,1,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,1,0,0,1,2,0,0,2,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,1,0,0,2,0],[0,0,0,0,0,2,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,2,0,0,0,0,0,0,0,0,0,0,0,1,2,0,0,0,0,0,2,0,0,0,0,0,0,0],[0,0,0,0,2,0,0,0,1,1,0,0,0,0,0,0,2,0,0,2,0,0,0,1,1,0,0,0,0,2,0,0,2,0,2,0,2,0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,2,0,0,2,0,1]]
    print(s.shortestDistance(grid))