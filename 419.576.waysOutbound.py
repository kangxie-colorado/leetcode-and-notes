"""
https://leetcode.com/problems/out-of-boundary-paths/

okay.. recursive DP? 
f(x,y,moveLeft) -- if it is 3D... maybe not easy to come up bottom up


"""


class Solution:
    def findPaths(self, m: int, n: int, maxMove: int, startRow: int, startColumn: int) -> int:
        mod = 10**9+7

        def f(x,y,movesLeft):
            if not (0<=x<m and 0<=y<n):
                return 1

            if movesLeft == 0:
                return 0
            
            res = f(x-1,y,movesLeft-1) + f(x+1,y,movesLeft-1) + f(x,y-1,movesLeft-1) + f(x,y+1,movesLeft-1)
            return res%mod
        return f(startRow, startColumn, maxMove)