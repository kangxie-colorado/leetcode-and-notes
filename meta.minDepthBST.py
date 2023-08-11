# Definition for a binary tree node.
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        
        def f(root):
            if not root.left and not root.right:
                return 0
            
            lDepth=rDepth=float('inf')
            if root.left:
                lDepth = f(root.left)
            if root.right:
                rDepth = f(root.right)
            
            return min(lDepth,rDepth) + 1
        
        return f(root)
    

"""
lessons:
1. didn't finish reading the examples, the depth is root to leafNode not to void
2. edge case, like empty tree
"""