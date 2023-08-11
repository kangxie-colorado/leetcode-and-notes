# Definition for a binary tree node.
from collections import deque
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
        
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:  
        if not root:
            return []
        q = deque()
        q.append(root)

        res = []
        while q:
            res.append(q[0].val)
            sz = len(q)
            while sz:
                node = q.popleft()
                sz -= 1
                if node.right:
                  q.append(node.right)
                if node.left:
                  q.append(node.left)
        
        return res
    

        
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:  
        q = deque()
        q.append(root)

        res = []
        while q:
            if q[0]:
                res.append(q[0].val)
            sz = len(q)
            while sz:
                node = q.popleft()
                sz -= 1
                if not node:
                    continue
                
                if node.right:
                  q.append(node.right)
                if node.left:
                  q.append(node.left)
        
        return res
    

# the form is not good