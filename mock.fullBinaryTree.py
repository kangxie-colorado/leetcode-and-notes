"""
the key is full binary tree
it must be 2^n - 1

1 cannot (1 can)
2 cannot 
4 cannot

divided into 3 parts
1 root
left 2^i - 1
right 2^j - 1

ah no.. 
5 can, so not 2^n - 1
2*n - 1???

"""

# Definition for a binary tree node.
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def allPossibleFBT(self, n: int) -> List[Optional[TreeNode]]:
        if n%2==0:
            return None

        def build(start, end):
            if start == end:
                return TreeNode()
            
            res = []
            for idx in range(start+1, end, 2):
                lefts = build(start, idx-1)
                rights = build(idx+1, end)
                
                for left in lefts:
                    for right in rights:
                        res.append(TreeNode(0,left,right))
            return res
        return build(1,n)
                
                
            