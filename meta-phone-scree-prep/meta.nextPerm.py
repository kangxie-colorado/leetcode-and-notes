from typing import List

class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        if len(nums) < 2:
            return
        
        # find the break point
        decrease = False
        for i in range(len(nums)-2,-1,-1):    
            if nums[i] < nums[i+1]:
                decrease = True
                break
        
        if i==0 and not decrease:
            nums.sort()
            return

        # find the swap num
        for j in range(len(nums)-1, i, -1):
            if nums[j] > nums[i]:
                break

        nums[i], nums[j] = nums[j], nums[i]
        nums[i+1:] = sorted(nums[i+1:])
            
    
if __name__ == '__main__':
  s = Solution()    
  nums = [1,2]
  s.nextPermutation(nums)

  print(nums)


        

                
            