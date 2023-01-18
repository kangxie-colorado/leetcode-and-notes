"""
https://leetcode.com/problems/maximum-side-length-of-a-square-with-sum-less-than-or-equal-to-threshold/?envType=study-plan&id=binary-search-ii

prefix sum 2D and binary search 

matrix sum part can be taken care by prefix pre-calculation 
then binary search the side-length see if I can find one
"""


import itertools
from typing import List


class Solution:

    def maxSideLength(self, mat: List[List[int]], threshold: int) -> int:
        

        m,n = len(mat), len(mat[0])
        matrixSums = [[0]*(n+1) for _ in range(m+1)]

        for i in range(1, m+1):
            matrixSums[i][1:] = list(itertools.accumulate(mat[i-1]))
            for j in range(1, n+1):
                matrixSums[i][j] += matrixSums[i-1][j]

        def exists(sl):
            for x1 in range(1, m+1):
                for y1 in range(1, n+1):
                    x2,y2 = x1+sl-1, y1+sl-1
                    if x2<=m and y2<=n:
                        sumSquare = matrixSums[x2][y2] - matrixSums[x1-1][y2] - matrixSums[x2][y1-1] + matrixSums[x1-1][y1-1]
                        if sumSquare <= threshold:
                            return True
            return False


        l,r = 0, min(m,n)
        while l<r:
            sideLen = r-(r-l)//2
            if exists(sideLen):
                l = sideLen
            else:
                r = sideLen-1
        return l

"""
Runtime: 1079 ms, faster than 74.36% of Python3 online submissions for Maximum Side Length of a Square with Sum Less than or Equal to Threshold.
Memory Usage: 19.3 MB, less than 83.97% of Python3 online submissions for Maximum Side Length of a Square with Sum Less than or Equal to Threshold.

alert when you use m named variable... I am burnt a few times to use it to mean rows/mid in binsect/target of valid function
"""

if __name__ == '__main__':
    s = Solution()
    # print(s.maxSideLength(mat = [[1,1,3,2,4,3,2],[1,1,3,2,4,3,2],[1,1,3,2,4,3,2]], threshold = 4))
    print(s.maxSideLength([[18, 70], [61, 1], [25, 85], [14, 40], [11, 96], [97, 96], [63, 45]],40184))
    