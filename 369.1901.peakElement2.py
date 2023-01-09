"""
https://leetcode.com/problems/find-a-peak-element-ii/


I have no idea of this one
but did solve the simpler version.. so I read the discussion 

2D.. if you think one column as a number.. then it simply becomes the 1D problem again
but do you have to scan all rows for any column.. not really

just scan the mid-column 
its max is already the max on that column.. just need to find an element that is col max and also >left and >right 

visualization of max per column is easier to be compared to 1D problem
but compute max per row is easier 

so we also can compare max-per-row and find a spot that is row max and also >up and > down.. 
let me code it up 

review the 1D problem first 
"""


from typing import List


class Solution:
    def findPeakElement(self, nums: List[int]) -> int:

        l,r = 0, len(nums)-1
        while l<r:
            m = l+(r-l)//2
            leftVal = nums[m-1] if m-1>=0 else float('-inf')
            rightVal = nums[m+1] if m+1<len(nums) else float('-inf')

            if leftVal < nums[m] and nums[m] > rightVal:
                return m
            elif nums[m] < rightVal:
                # a bigger val exists to the right 
                # chance is also a bigger val exists to the left.. but search any direction is okay
                l = m+1
            else:
                # this includes the nums[m] >= right 
                r = m-1
        return l
"""
Runtime: 49 ms, faster than 84.99% of Python3 online submissions for Find Peak Element.
Memory Usage: 14 MB, less than 81.99% of Python3 online submissions for Find Peak Element.
"""


class Solution:
    def findPeakGrid(self, mat: List[List[int]]) -> List[int]:

        minRow, maxRow = 0, len(mat)-1

        while minRow < maxRow:

            midRow = minRow + (maxRow-minRow)//2
            rowMax, idx = mat[midRow][0], 0
            for j, n in enumerate(mat[midRow]):
                if n > rowMax:
                    rowMax = n
                    idx = j

            upVal = mat[midRow-1][idx] if midRow >= 1 else float('-inf')
            downVal = mat[midRow+1][idx] if midRow + \
                1 < len(mat) else float('-inf')

            if upVal < rowMax and rowMax > downVal:
                return [midRow, idx]
            elif rowMax < downVal:
                # a bigger val exists in the bottom
                minRow = midRow+1
            else:
                maxRow = midRow-1

        # print(minRow)
        rowMax, idx = mat[minRow][0], 0
        for j, n in enumerate(mat[minRow]):
            if n > rowMax:
                rowMax = n
                idx = j
        return [minRow, idx]


"""
Runtime: 2871 ms, faster than 41.63% of Python3 online submissions for Find a Peak Element II.
Memory Usage: 45.5 MB, less than 45.52% of Python3 online submissions for Find a Peak Element II.
"""

class Solution:
    def findPeakGrid(self, mat: List[List[int]]) -> List[int]:
        top = 0
        bottom = len(mat)-1
        while bottom > top:
            mid = (top + bottom) // 2
            if max(mat[mid]) > max(mat[mid+1]):
                bottom = mid
            else:
                top = mid+1
        return [bottom,mat[bottom].index(max(mat[bottom]))]

"""
ah... ha.. this is clever 
and still O(lgn * n)

and faster than my own
Runtime: 1797 ms, faster than 55.84% of Python3 online submissions for Find a Peak Element II.
Memory Usage: 45.4 MB, less than 78.17% of Python3 online submissions for Find a Peak Element II.
"""

# okay.. this is cleaner.. let minRow==maxRow to do one more run


class Solution:
    def findPeakGrid(self, mat: List[List[int]]) -> List[int]:

        minRow, maxRow = 0, len(mat)-1

        while minRow <= maxRow:

            midRow = minRow + (maxRow-minRow)//2
            rowMax, idx = mat[midRow][0], 0
            for j, n in enumerate(mat[midRow]):
                if n > rowMax:
                    rowMax = n
                    idx = j

            upVal = mat[midRow-1][idx] if midRow >= 1 else float('-inf')
            downVal = mat[midRow+1][idx] if midRow + \
                1 < len(mat) else float('-inf')

            if upVal < rowMax and rowMax > downVal:
                return [midRow, idx]
            elif rowMax < downVal:
                # a bigger val exists in the bottom
                minRow = midRow+1
            else:
                maxRow = midRow-1

"""
Runtime: 1653 ms, faster than 59.39% of Python3 online submissions for Find a Peak Element II.
Memory Usage: 45.3 MB, less than 78.17% of Python3 online submissions for Find a Peak Element II.

"""