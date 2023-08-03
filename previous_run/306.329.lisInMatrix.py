"""


"""


from typing import List


class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        m, n = len(matrix), len(matrix[0])
        dp = [[]]*m
        for i in range(m):
            dp[i] = [0]*n

        def dfs(x, y, path, pVal):
            if x < 0 or y < 0 or x >= m or y >= n or matrix[x][y] <= pVal:
                return 0

            if dp[x][y] != 0:
                return dp[x][y]

            if (x, y) in path:
                return 0
            path.add((x, y))

            up = dfs(x-1, y, path, matrix[x][y])
            down = dfs(x+1, y, path, matrix[x][y])
            left = dfs(x, y-1, path, matrix[x][y])
            right = dfs(x, y+1, path, matrix[x][y])

            dp[x][y] = max(left, right, up, down) + 1
            return dp[x][y]

        res = 0
        for i in range(m):
            for j in range(n):
                dp[i][j] = dfs(i, j, set(), -1)
                res = max(res, dp[i][j])
        return res


"""
okay.. this dp+memorization is easy to understand 
I see the post by that girl who can both program and dance..
https://leetcode.com/problems/longest-increasing-path-in-a-matrix/discuss/288520/Longest-Path-in-DAG

it is kind of genius 
so I want to convert that idea into my own code as well

I think she works from the smallest spot upward ... using inwards degrees.. 0 means nothing is smaller 
if there is nothing smaller around, then it is the smallest spot locally .. add it to the processing queue

go thru the queue.. 
for its neighbors, which must be greater than it (euqal ones are equal smallest spot).. reduce their in-degree by one

if their indegree reaches 0, then they becomes the smaller spot (after processing surrounding spot)
adding them to next processing queue (or snapshot the size of current queue and go thru only that much.. just enough to go around)

add the lis lenght by 1..

continue to next queue
it is like peeling thru layers but in this unorganized way...

"""


class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        m, n = len(matrix), len(matrix[0])
        indegree = [[]]*m
        for i in range(m):
            indegree[i] = [0]*n

        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for x in range(m):
            for y in range(n):
                for dx, dy in dirs:
                    x2, y2 = x+dx, y+dy
                    if 0 <= x2 <= m-1 and 0 <= y2 <= n-1 and matrix[x2][y2] < matrix[x][y]:
                        indegree[x][y] += 1

        q = []
        for x in range(m):
            for y in range(n):
                if indegree[x][y] == 0:
                    q.append((x, y))

        lisLen = 0
        while q:
            sz = len(q)  # taking a snapshot so no need to copy/replace
            while sz:
                x, y = q[0]
                q = q[1:]

                for dx, dy in dirs:
                    x2, y2 = x+dx, y+dy
                    if 0 <= x2 <= m-1 and 0 <= y2 <= n-1 and matrix[x2][y2] > matrix[x][y]:
                        indegree[x2][y2] -= 1
                        if indegree[x2][y2] == 0:
                            q.append((x2, y2))
                sz -= 1
            lisLen += 1
        return lisLen


"""
Runtime: 816 ms, faster than 66.38% of Python3 online submissions for Longest Increasing Path in a Matrix.
Memory Usage: 14.9 MB, less than 82.62% of Python3 online submissions for Longest Increasing Path in a Matrix.

cool.. 
looking back.. it seems like she is focusing on the indegress == 0 spots i.e. the smallest spot
after that gets processed.. the new spots might emerge..

because this can be thought as DAG the strict > relationship forms. 
also each round we look to find bigger number (and decrease their indegree) by matrix[x2][y2] > matrix[x][y]
so never will end up in a loop 

going thru each layer, the lis += 1
it is kind of intrisic but hard to put to precise words

"""

if __name__ == '__main__':
    s = Solution()
    print(s.longestIncreasingPath([[7, 7, 5], [2, 4, 6], [8, 2, 0]]))
