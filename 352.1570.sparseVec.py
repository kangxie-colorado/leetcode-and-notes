"""
https://leetcode.com/problems/dot-product-of-two-sparse-vectors/?envType=study-plan&id=programming-skills-iii
"""





from typing import List


class SparseVector:
    def __init__(self, nums: List[int]):
        self.m = {i:n for i,n in enumerate(nums) if n!= 0}


    # Return the dotProduct of two sparse vectors
    def dotProduct(self, vec: 'SparseVector') -> int:
        this = set(self.m.keys())
        other = set(vec.m.keys())
        res = 0
        for k in this.intersection(other):
            res += self.m[k] * vec.m[k]

        return 
        
"""
Runtime: 1692 ms, faster than 99.01% of Python3 online submissions for Dot Product of Two Sparse Vectors.
Memory Usage: 18.4 MB, less than 53.40% of Python3 online submissions for Dot Product of Two Sparse Vectors.

Runtime: 1805 ms, faster than 89.45% of Python3 online submissions for Dot Product of Two Sparse Vectors.
Memory Usage: 18.2 MB, less than 66.64% of Python3 online submissions for Dot Product of Two Sparse Vectors.
"""