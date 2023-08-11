# https://leetcode.com/problems/number-of-black-blocks/

from collections import defaultdict
from typing import List


class Solution:
  def countBlackBlocks(self, m: int, n: int, coordinates: List[List[int]]) -> List[int]:
    mat = [[0]*n for _ in range(m)]
    for x,y in coordinates:
      if x-1>=0 and y-1>=0:
        mat[x-1][y-1] += 1
      if x-1>=0 and y+1<n:
        mat[x-1][y] += 1
      if y-1>=0 and x+1<m:
        mat[x][y-1]+=1
      if x+1<m and y+1<n:
        mat[x][y] += 1
    
    blockCounts = [0]*5
    for i in range(m):
      for j in range(n):
        blockCounts[mat[i][j]] += 1
    
    blockCounts[0] = (m-1)*(n-1) - sum(blockCounts[1:])
    return blockCounts

"""
TLE
"""

class Solution:
  def countBlackBlocks(self, m: int, n: int, coordinates: List[List[int]]) -> List[int]:
    mat = [[0]*n for _ in range(m)]
    blocks = set()
    for x,y in coordinates:
      if x-1>=0 and y-1>=0:
        mat[x-1][y-1] += 1
        blocks.add((x-1,y-1))
      if x-1>=0 and y+1<n:
        mat[x-1][y] += 1
        blocks.add((x-1,y))
      if y-1>=0 and x+1<m:
        mat[x][y-1]+=1
        blocks.add((x,y-1))
      if x+1<m and y+1<n:
        mat[x][y] += 1
        blocks.add((x,y))
    
    blockCounts = [0]*5
    for i,j in blocks:
        blockCounts[mat[i][j]] += 1
    
    blockCounts[0] = (m-1)*(n-1) - sum(blockCounts[1:])
    return blockCounts
  
  """
  TLE
  """

class Solution:
  def countBlackBlocks(self, m: int, n: int, coordinates: List[List[int]]) -> List[int]:
    blocks = defaultdict(int)
    for x,y in coordinates:
      if x-1>=0 and y-1>=0:
        blocks[(x-1)*n+y-1] +=1 
      if x-1>=0 and y+1<n:
        blocks[(x-1)*n+y] +=1 
      if y-1>=0 and x+1<m:
        blocks[x*n+y-1] +=1 
      if x+1<m and y+1<n:
        blocks[x*n+y] +=1 
    
    blockCounts = [0]*5
    for coord in blocks:
        blockCounts[blocks[coord]] += 1
    
    blockCounts[0] = (m-1)*(n-1) - sum(blockCounts[1:])
    return blockCounts
  
"""
Runtime: 1716 ms, faster than 100.00% of Python3 online submissions for Number of Black Blocks.
Memory Usage: 24.2 MB, less than 82.57% of Python3 online submissions for Number of Black Blocks.
"""

if __name__ == '__main__':
  s = Solution()
  print(s.countBlackBlocks(m = 3, n = 3, coordinates = [[0,0]]))
  print(s.countBlackBlocks(m = 3, n = 3, coordinates = [[0,0],[1,1],[0,2]]))