from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        
        res = []
        for i in range(len(nums)):
            if i>0 and nums[i] == nums[i-1]:
                continue

            twoSum = 0 - nums[i]
            j,k = i+1, len(nums)-1
            while j<k:
              if nums[j] + nums[k] == twoSum:
                  res.append([nums[i], nums[j], nums[k]])

                  j,k = j+1,k-1
                  while j<len(nums) and nums[j] == nums[j-1]:
                      j+=1
                  while k>0 and nums[k] == nums[k+1]:
                      k-=1
              elif nums[j] + nums[k] < twoSum:
                  j+=1
              else:
                  k-=1
        
        return res

            




