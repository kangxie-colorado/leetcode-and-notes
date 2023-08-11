

from typing import List


class NumMatrix:

    def __init__(self, matrix: List[List[int]]):
        m,n = len(matrix), len(matrix[0])
        sumMat = [[0]*(n+1) for _ in range(m+1)]

        for r in range(1,m+1):
            for c in range(1, n+1):
                sumMat[r][c] = sumMat[r][c-1] + matrix[r-1][c-1]
        
        for r in range(1,m+1):
            for c in range(1, n+1):
                sumMat[r][c] += sumMat[r-1][c]
        
        self.sumMat = sumMat

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        
        return self.sumMat[row2+1][col2+1] - self.sumMat[row1][col2+1] - self.sumMat[row2+1][col1] + self.sumMat[row1][col1]


# Your NumMatrix object will be instantiated and called as such:
# obj = NumMatrix(matrix)
# param_1 = obj.sumRegion(row1,col1,row2,col2)


"""
https://leetcode.com/problems/range-sum-query-2d-immutable/discuss/75350/Clean-C%2B%2B-Solution-and-Explaination-O(mn)-space-with-O(1)-time

aha.. when I was calculating the region sum, there is a duplicate compute which I don't know how to get rid of
so i did the loop twice but it can be done in one pass..

the key is to notice that the left up corner was added twice.. 
just like when you do the substraction, it will be substracted twice...

sumMat[r][c] = sumMat[r][c-1] + matrix[r-1][c-1] + sumMat[r-1][c] - sumMat[r-1][c-1]

this is great! 

if I am able to draw that picture.. maybe I can figure out.. 
but when you don't know, you don't know
"""

class NumMatrix:

    def __init__(self, matrix: List[List[int]]):
        m,n = len(matrix), len(matrix[0])
        sumMat = [[0]*(n+1) for _ in range(m+1)]

        for r in range(1,m+1):
            for c in range(1, n+1):
                sumMat[r][c] = sumMat[r][c-1] + matrix[r-1][c-1] + sumMat[r-1][c] - sumMat[r-1][c-1]
        
        self.sumMat = sumMat

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        
        return self.sumMat[row2+1][col2+1] - self.sumMat[row1][col2+1] - self.sumMat[row2+1][col1] + self.sumMat[row1][col1]

"""
Runtime: 1133 ms, faster than 94.96% of Python3 online submissions for Range Sum Query 2D - Immutable.
Memory Usage: 26.9 MB, less than 87.42% of Python3 online submissions for Range Sum Query 2D - Immutable.
"""


if __name__ == '__main__':
    calls = ["NumMatrix","sumRegion","sumRegion","sumRegion"]
    params = [[[[3,0,1,4,2],[5,6,3,2,1],[1,2,0,1,5],[4,1,0,1,7],[1,0,3,0,5]]],[2,1,4,3],[1,1,2,2],[1,2,2,4]]

    for call,param in zip(calls, params):
        if call == 'NumMatrix':
            nm = NumMatrix(*param)
        else:
            print(nm.sumRegion(*param))