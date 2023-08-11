
from collections import defaultdict
from typing import List


class SparseVector:
    def __init__(self, nums: List[int]):
        self.nums = nums

    # Return the dotProduct of two sparse vectors
    def dotProduct(self, vec: 'SparseVector') -> int:
        res = 0
        for num1, num2 in zip(self.nums, vec.nums):
            res += num1*num2
        
        return res
        

# Your SparseVector object will be instantiated and called as such:
# v1 = SparseVector(nums1)
# v2 = SparseVector(nums2)
# ans = v1.dotProduct(v2)

class SparseVector:
    def __init__(self, nums: List[int]):
        self.nums = defaultdict(int)
        for idx,num in enumerate(nums):
            if num!=0:
                self.nums[idx] = num
        

    # Return the dotProduct of two sparse vectors
    def dotProduct(self, vec: 'SparseVector') -> int:
        res = 0
        for idx,num in self.nums.items():
            res += num * vec.nums[idx]
        return res
  

if __name__ == '__main__':
    sv1 = SparseVector([1,0,0,2,3])
    sv2 = SparseVector([0,3,0,4,0])

    print(sv1.dotProduct(sv2))