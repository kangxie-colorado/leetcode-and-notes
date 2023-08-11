from typing import List

from sortedcontainers import SortedList


class Solution:
  def maxIncreasingCells(self, mat: List[List[int]]) -> int:
    # global sorting order
    # processing from smallest to largest; deal with each row and column
    # if I have an ordered dict? but it doesn't support finding the smaller element
    # otherwise, just use the SortedList and save a tuple
    m,num = len(mat), len(mat[0])
    allNums = sorted([(mat[i][j], i, j) for i in range(m)
                        for j in range(num)])

    rows = [SortedList() for i in range(m)]
    cols = [SortedList() for j in range(num)]
    for row in rows:
      row.add([float("-inf"), 0])
    for col in cols:
      col.add([float("-inf"), 0])

    res = 0
    for num,row,col in allNums:
      rPrev = rows[row].bisect_left([num,0])-1
      cPrev = cols[col].bisect_left([num,0])-1
      l = max(rows[row][rPrev][1]+1, cols[col][cPrev][1]+1)

      if rPrev+1<len(rows[row]) and rows[row][rPrev+1][0] == num:
        # this number is already in list
        rows[row][rPrev+1][1] = max(l, rows[row][rPrev+1][1])
      else:
        rows[row].add([num,l])

      if cPrev+1<len(cols[col]) and cols[col][cPrev+1][0] == num:
        cols[col][cPrev+1][1] = max(l, cols[col][cPrev+1][1])
      else:
        cols[col].add([num,l])
      
      res = max(res, l)
    
    return res

if __name__ == '__main__':
  S = Solution()
  print(S.maxIncreasingCells([[3,1],[3,4]]))
  print(S.maxIncreasingCells([[3,1,6],[-9,5,7]]))
  a = [[4,-6,2],[-7,8,6],[1,2,-3],[-6,5,5],[5,-4,3]]
  print(S.maxIncreasingCells(a))