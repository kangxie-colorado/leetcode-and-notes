# https://leetcode.com/problems/special-permutations/

"""
dp..
the trick is to notice the nums.length is small -- so bitmap can be used
bitmap can replace the permutations as one of the state variable
otherwise, a set cannot be the state variable because it cannot be key of cache...

"""

from functools import cache
from typing import List


class Solution:
  def specialPerm(self, nums: List[int]) -> int:
    def numOfOnes(num):
      res = 0
      # this is to eliminate the lowest 1 bit
      while num:
        num &= num - 1
        res += 1

      return res

    m = len(nums)
    mod = 1_000_000_000 + 7

    @cache
    def f(lastIdx, bm):
      """
      lastIdx:
        the index in nums for last number, used to constrain next numbers choice
        -1 means none has been chose yet
      bm(bitmap):
        used to record the chosen indexes, meaning unused indexes can be chose in this run
        at most 2^m-1
      """
      if numOfOnes(bm) == len(nums):
        return 1

      res = 0
      if lastIdx == -1:
        for i in range(m):
          res += f(i, 1 << i)
          res %= mod
        return res

      for i in range(m):
        if 1 << i & bm:
          continue
        if nums[lastIdx] % nums[i] == 0 or nums[i] % nums[lastIdx] == 0:
          res += f(i, bm | (1 << i))
          res %= mod

      return res

    return f(-1, 0)
  
"""
Runtime: 4243 ms, faster than 64.19% of Python3 online submissions for Special Permutations.
Memory Usage: 223 MB, less than 18.69% of Python3 online submissions for Special Permutations.
"""

if __name__ == '__main__':
  s = Solution()
  print(s.specialPerm(nums = [2,3,6]))