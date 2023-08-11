from typing import List


class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        i=j=0
        while True:
            while i<len(nums) and nums[i]!=0:
                i+=1
            
            while j< len(nums) and nums[j]==0:
                j+=1
            
            if j>= len(nums) or i>=len(nums):
                break
            
            if j>=i:
              nums[i],nums[j] = nums[j], nums[i]

"""
this will fail [1,0]
"""

class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        i=0
        while True:
          while i<len(nums) and nums[i]!=0:
              i+=1
          
          j=i
          while j< len(nums) and nums[j]==0:
              j+=1
              
          if j>= len(nums):
              break
          
          if j>=i:
            nums[i],nums[j] = nums[j], nums[i]

if __name__ == '__main__':
    s = Solution()
    nums = [1,0]
    s.moveZeroes(nums)
    print(nums)