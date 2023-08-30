"""

class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        if len(nums1)>len(nums2):
            nums1,nums2 = nums2,nums1
        
        res = []
        takenmeta
        for num1 in nums1:
            if num1 in nums2:
                res.append(num1)
        
        return res


I wrote this and quickly found out I am wrong
Input
[3,1,2]
[1,1]
Output
[1,1]
Expected
[1]

so lessons learned:
1. not that easy.. do think it carefully before jumping
Each element in the result must appear as many times as it shows in both arrays
read the problem.. appearing in both arrays
"""

from collections import Counter
from typing import List


class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        C1 = Counter(nums1)
        C2 = Counter(nums2)

        res = []
        for num,count in C1.items():
            if num in C2:
                res.extend([num]*min(count, C2[num]))
        
        return res
  
if __name__ == '__main__':
    s = Solution()
    print(s.intersect(nums1 = [1,2,2,1], nums2 = [2,2]))