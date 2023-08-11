from collections import defaultdict
from typing import List


"""
equal oppurtunity
then I just go one by one.. keeping an crusor
"""

class Solution:

    def __init__(self, nums: List[int]):
      self.nums = nums
      self.numToIdxes = defaultdict(list)
      self.numCurrIdx = defaultdict(int)
      for idx,num in enumerate(nums):
          self.numToIdxes[num].append(idx)
          self.numCurrIdx[num] = 0

    def pick(self, target: int) -> int:
        ret = self.numToIdxes[target][self.numCurrIdx[target]]
        self.numCurrIdx[target] += 1
        self.numCurrIdx[target] %= len(self.numToIdxes[target])

        return ret


# Your Solution object will be instantiated and called as such:
# obj = Solution(nums)
# param_1 = obj.pick(target)