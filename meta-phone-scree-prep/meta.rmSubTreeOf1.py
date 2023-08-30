# Definition for a binary tree node.
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

        
class Solution:
    def pruneTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        
        # return True if subtree has 1
        # return False if not
        # if subtree has no 1, remove the subtree
        def f(root):
            if not root.left and not root.right:
                return root.val == 1
            
            leftHas1 = rightHas1 = False
            if root.left:
              leftHas1 = f(root.left)
              if not leftHas1:
                  root.left = None
            
            if root.right:
                rightHas1 = f(root.right)
                if not rightHas1:
                    root.right = None
            
            return leftHas1 or rightHas1 or root.val==1
        
        if f(root):
          return root
        
        return None

            
            