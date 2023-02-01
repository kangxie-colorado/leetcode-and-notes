"""
https://leetcode.com/problems/strange-printer-ii/?envType=study-plan&id=graph-ii

I am tired enough today so not gonna to write code but only jot down some notes before I forget
I want to write what I struggled with and how I broke through 

so it is visible the smaller rectangle should be printed later than bigger ones, if they overlap
so this is kind of a topological sort problem 

then the issue is how to establish the dependencies 
first I thought I can define the rectangle with some width/height/left-up and then see if another rectangle falls 
intot its boundary -- if yes, then overlap 

then this form baffled me for a while
1 1 1 1
1 2 1 1
1 1 2 1
1 1 1 1

this apparently cannot be printed okay
but how to model it?

I thought to test if a color is connected component, if not.. then not possible? but then the example 1 denies me this idea
the 1 is disconnected 

then I thought okay.. 
    - go thru the matrix, record each rectangle's max/min x and max/min y 
    - then in that min/max x/y, search for the colors, any color inside will be depending on this rectangle 
    it is getting close but still very troublesome to do this

then I thought
    - sitll go thru the matrix, estalish every color's min/max x/y
    - go thru again
        if this color falls into some rectangle, then this color depends on that rectangle's color
        it could be its self.. then that is ignored 
    - after establishing the dependency graph. the topo sort can be run with dfs or bfs

so in above example
    1: [     x  y
        min: 0  0
        max  3  3
    ]
    2: [     x  y
        min: 1  1
        max  2  2
    ]

when search you will find 1 -> 2 and 2 -> 1.. so it is not possible
okay.. so much for today.. continue tomorrow

"""


from collections import defaultdict, deque
from typing import List

def defaultBoundary():
    return [float('inf'),float('-inf'),float('inf'),float('-inf')]


class Solution:
    def isPrintable(self, A: List[List[int]]) -> bool:
        m,n = len(A), len(A[0])
        colors =  defaultdict(defaultBoundary) # color: [minX, maxX, minY, maxY]
        maxColor = 0
        
        # scan for color boundaries 
        for i in range(m):
            for j in range(n):
                color = A[i][j]
                maxColor = max(maxColor, color)
                minX,maxX,minY,maxY = colors[color]
                colors[color] = [
                    min(minX, i),
                    max(maxX, i),
                    min(minY, j),
                    max(maxY, j)
                ]
        
        # establish the dependency mapping
        graphs = defaultdict(set)
        incomingLinks = [0] * (maxColor+1)
        for i in range(m):
            for j in range(n):
                insideColor = A[i][j]
                for outsideColor in colors:
                    if outsideColor == insideColor:
                        continue
                    minX, maxX, minY, maxY = colors[outsideColor]
                    if minX <= i <= maxX and minY <= j <= maxY:
                        # we see this color depends on c
                        # we add the arrow from c->color
                        # note we can only add once (for the incoming links counting)
                        if insideColor not in graphs[outsideColor]:
                            graphs[outsideColor].add(insideColor)
                            incomingLinks[insideColor] += 1
        
        # bfs to sort topologically
        bfsQueue = deque()
        for color in range(len(incomingLinks)):
            if incomingLinks[color] == 0 and color in colors:
                bfsQueue.append(color)
        
        painted = 0
        while bfsQueue:
            sz = len(bfsQueue)
            while sz:
                color = bfsQueue.popleft()
                painted += 1
                for nextColor in graphs[color]:
                    incomingLinks[nextColor] -= 1
                    if incomingLinks[nextColor] == 0:
                        bfsQueue.append(nextColor)
                
                sz-=1
        return painted == len(colors)


"""
Runtime: 3276 ms, faster than 5.60% of Python3 online submissions for Strange Printer II.
Memory Usage: 14.3 MB, less than 40.80% of Python3 online submissions for Strange Printer II.

Runtime: 745 ms, faster than 50.40% of Python3 online submissions for Strange Printer II.
Memory Usage: 14.2 MB, less than 89.60% of Python3 online submissions for Strange Printer II.

as always, Lee has a different solution.. which I don't understand but kind of feel it is same
if I have time or come across this again, I can check it out
"""


if __name__ == '__main__':
    s = Solution()
    print(s.isPrintable(A = [[1,1,1,1],[1,1,3,3],[1,1,3,4],[5,5,1,4]]))
    print(s.isPrintable(A = [[1,2,1],[2,1,2],[1,2,1]]))