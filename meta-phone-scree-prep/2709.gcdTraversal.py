# https://leetcode.com/problems/greatest-common-divisor-traversal/

from typing import List


class Solution:
  def canTraverseAllPairs(self, nums: List[int]) -> bool:
    if nums == [1]: return True
    nums = list(set(nums))
    if any(nums[i]==1 for i in range(len(nums))): return False
    
    def allPrimsUnder(n):
      nums = [1]*(n+1)
      nums[:2] = [0,0]

      for idx in range(2,n+1):
          if nums[idx] == 1:
              multiple = 2
              while multiple*idx<n+1:
                  nums[idx*multiple]=0
                  multiple+=1
      return [i for i,n in enumerate(nums) if n]    
    allPrims = allPrimsUnder(max(nums))

    roots = {}
    def find(x):
        roots.setdefault(x,x)
        if roots[x] != x:
            roots[x] = find(roots[x])
        return roots[x]
    
    def union(x1,x2):
        roots[find(x1)] = roots[find(x2)]
    
    for idx,num in enumerate(nums):
       for p in allPrims:
          if p>num: break

          if num%p==0:
             union(nums[idx], p)
             while num%p==0:
                num//=p
    
    rootGroup = set()
    for num in nums:
       rootGroup.add(find(num))
      
    return len(rootGroup)==1

"""
Runtime: 8890 ms, faster than 11.42% of Python3 online submissions for Greatest Common Divisor Traversal.
Memory Usage: 35.4 MB, less than 59.68% of Python3 online submissions for Greatest Common Divisor Traversal.
"""


if __name__ == '__main__':
   s = Solution()
   print(s.canTraverseAllPairs([2,3,6]))
   print(s.canTraverseAllPairs([3,9,5]))
   print(s.canTraverseAllPairs([4,3,12,8]))

