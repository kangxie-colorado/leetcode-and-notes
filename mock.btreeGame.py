"""
it feels so difficult 
but when you think it carefully

it boils down to 
1. tree root at x, has left than half - I only need to block the parent (if it has a parent, not root)
2. x.left, x.right has more than half - I only need to block that sub-tree
"""

# Definition for a binary tree node.
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

        
class Solution:
    def btreeGameWinningMove(self, root: Optional[TreeNode], n: int, x: int) -> bool:
        
        counts = {}
        def f(root):
            if not root:
                return 0
            
            leftCount = f(root.left)
            rightCount = f(root.right)
            counts[root.val] = (leftCount+rightCount+1, leftCount, rightCount)
            return leftCount+rightCount+1
        
        f(root)

        if counts[x][0]*2 < n or counts[x][1]*2 > n or counts[x][2]*2 > n:
            return True

        return False 
