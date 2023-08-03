"""
https://leetcode.com/problems/cherry-pickup/?envType=study-plan&id=dynamic-programming-iii

feel like should not be very difficult but low ac ratio so I don't know

it feels like to find two paths
    the first path with most cherries 
    then finding the next path with most cherries... (with cherries on first one marked..)

using dp I can find the max cherry picked up then I back trace it to build the trace.. and keep it out of the 2nd path way???
it could work.. give a try

"""


from typing import List


class Solution:
    def cherryPickup(self, grid: List[List[int]]) -> int:
        n = len(grid)
        def buildOnePath():
            dp = [[-1]*n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    if i==0 and j==0:
                        dp[i][j] = grid[i][j]
                        continue

                    if grid[i][j] != -1:
                        upVal = dp[i-1][j] if i > 0 else -1
                        leftVal = dp[i][j-1] if j > 0 else -1
                        if upVal==leftVal==-1:
                            dp[i][j] = -1
                        else:
                            dp[i][j] = max(upVal, leftVal) + grid[i][j]
            return dp

        dp = buildOnePath()
        
        if dp[n-1][n-1] == -1:
            return 0

        # retrace to build up the first path 
        pathNode = (n-1,n-1)
        path = set()
        while pathNode != (0,0):
            path.add(pathNode)
            x,y = pathNode
            
            upVal = dp[x-1][y] if x>0 else -1
            leftVal = dp[x][y-1] if y>0 else -1

            if upVal > leftVal:
                pathNode = (x-1,y)
            else:
                pathNode = (x, y-1)
        path.add((0,0))

        # mark that path off
        for x,y in path:
            grid[x][y] = 0
        
        dp2 = buildOnePath()
        return dp[n-1][n-1] + dp2[n-1][n-1]

"""
49/59 cases passed 
[[1,1,1,1,0,0,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,1],[1,0,0,1,0,0,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,0],[0,0,0,1,1,1,1]]
okay.. it doesn't have to go the most cherry path
in this case.. it takes sub-optimal path but the two path sum > the greedy paths sum...

1 1 1
0 1 0

still following the 2 path logical
to reach the end.. if walk twice it can actually cover all 4

how to model?????

okay.. I never expanded my mind enough to think of 3D/4D dp... 
3D maybe.. but 4D.. ugh..

so this is a 4D/3D 
basically my early insights about this basically making two walks from 0,0 to n-1,n-1 is right
but how to model that?

well...
you model one path with dp[i][j]
you can model two path with dp[x][y]

since two paths need to happen in parallel (that is why this is a squre.. not a rectangle? hmmm.. not sure about that)
i+j === x+y (the manhattan distance to 0,0, and the steps it walked)

so it reduced to 3D
how the transition equation form?

dp[i][j][x][y]: represents total cherries with first path at ending i,j and 2nd path ending at x,y
what is its dependencies..

which is kind of trick to think 
                                (x-1,y)
         (i-1,j)        (x,y-1) (x,y)
(i,j-1)  (i,j)     

the two paths walk independently so
to reach i,j.. the first path needs to come from (i-1,j) or (i,j-1)
to reach x,y.. the 2nd path needs to come from (x-1,y) or (x,y-1)

they don't need to care for each other.. so indeed 4 pre-states (sub-problems)
dp[i][j][x] = max {
    dp[i-1][j][x] # y is ignored because i+j==x+y
    dp[i-1][j][x-1]
    dp[i][j-1][x]
    dp[i][j-1][x-1]
}

we open the dp to one row/colomn more 
for dp[1][1] we specialize it... 

could give a try before interview

"""


class Solution:
    def cherryPickup(self, grid: List[List[int]]) -> int:
        n = len(grid)

        dp = [[[float('-inf')]*(n+1) for _ in range(n+1)] for _ in range(n+1)]

        for i in range(1,n+1):
            for j in range(1,n+1):
                for x in range(1,n+1):
                    y = i+j-x
                    if y<1 or y>n:
                        continue
                        
                    if i==j==x==1:
                        dp[i][j][x] = grid[i-1][j-1]
                        continue

                    if grid[i-1][j-1]!=-1 and grid[x-1][y-1]!=-1:
                        dp[i][j][x] = max(
                            dp[i-1][j][x],
                            dp[i-1][j][x-1],
                            dp[i][j-1][x],
                            dp[i][j-1][x-1],
                        )

                        dp[i][j][x] += grid[i-1][j-1]
                        if (i,j) != (x,y):
                            dp[i][j][x] += grid[x-1][y-1]

        return max(0, dp[n][n][n])


if __name__ == '__main__':
    s = Solution()
    print(s.cherryPickup( grid = [[0,1,-1],[1,0,-1],[1,1,1]]))
    # print(s.cherryPickup( grid = [[1,1,-1],[1,-1,1],[-1,1,1]]))