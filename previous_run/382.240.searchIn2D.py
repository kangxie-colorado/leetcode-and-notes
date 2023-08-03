"""
https://leetcode.com/problems/search-a-2d-matrix-ii/?envType=study-plan&id=binary-search-ii

without doing that peak element
I might do it in O(n+m)

but now I think this can be sovled in O(lgn + lgm)

search in last row to decide the column?
hum... not really 

[1,4,7,11,15],
[2,5,8,12,19],
[3,6,9,16,22],
[10,13,14,17,24],
[18,21,23,26,30]

seach 13... in last colum.. it will be returned as column 0 and not find 
so where is the O(logN+logM)

okay probably can still only eliminate 1/4 of the matrix 
then it is still only the eliminate one row or one column method being the easist way to 
"""


import bisect
from typing import List


class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:

        for row in matrix:
            idx = bisect.bisect_left(row, target)
            if idx < len(row) and row[idx] == target:
                return True
        return False

"""
Runtime: 157 ms, faster than 99.74% of Python3 online submissions for Search a 2D Matrix II.
Memory Usage: 20.4 MB, less than 84.34% of Python3 online submissions for Search a 2D Matrix II.

well... this basic O(mlogn) is not bad at all
"""
