"""
https://leetcode.com/problems/unique-paths-ii/

still think.. it is almost the same as unique paths I
the only twist is when left/up is obstacle, don't add it or better just apply prod on it

"""


from typing import List


class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        m,n = len(obstacleGrid), len(obstacleGrid[0])
        if obstacleGrid[m-1][n-1]:
            return 0
        dp = [[0]*(n+1) for _ in range(m+1)]
        for i in range(1, m+1):
            for j in range(1, n+1):
                if i == 1 and j == 1:
                    dp[i][j] = 1
                    continue
                
                upObstacle = 1 if i>1 and obstacleGrid[i-2][j-1] else 0
                leftObstacle = 1 if j>1 and obstacleGrid[i-1][j-2] else 0

                dp[i][j] = dp[i-1][j]*(1-upObstacle) + dp[i][j-1]*(1-leftObstacle)
        return dp[m][n]

""""
[[0,0],[0,1]]
obstacel at the end.. --- bu jiang wu de

fix it and 
Runtime: 37 ms, faster than 97.04% of Python3 online submissions for Unique Paths II.
Memory Usage: 13.9 MB, less than 72.74% of Python3 online submissions for Unique Paths II.
"""