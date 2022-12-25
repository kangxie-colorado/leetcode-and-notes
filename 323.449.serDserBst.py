"""
https://leetcode.com/problems/serialize-and-deserialize-bst/?envType=study-plan&id=programming-skills-iii

I think I did this before use preorder + inorder
recently I learned that BST reconstruct from preorder can be done O(n)

it takes an optimism thinking like solution 
the first element is always the root of some subtree

create the root then pop it off 
then try creating left tree on next node if it does satisfy the min<val<max condition ... otherwise, this is not a node in this subtree
it recurse to upper level... and try treating it like right node... 




"""

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None


from collections import deque
from typing import Optional
from utils import TreeNode


class Codec:

    def serialize(self, root: Optional[TreeNode]) -> str:
        """Encodes a tree to a single string.
        """
        vals = []
        def preorder(node):
            if node:
                vals.append(node.val)
                preorder(node.left)
                preorder(node.right)
            
        preorder(root)
        return ",".join(vals)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        """Decodes your encoded data to tree.
        """
        preorder = deque(map(int, data.split()))

        def create(A, leftBound, rightBound):
            root = None
            if A and leftBound < A < rightBound:
                root = TreeNode(A[0])
                val = A.popleft()
                root.left = create(A, leftBound, val)
                root.right = create(A, val, rightBound)

            return root
        
        return create(preorder, -float('inf'), float('inf'))

"""
Runtime: 73 ms, faster than 96.43% of Python3 online submissions for Serialize and Deserialize BST.
Memory Usage: 18.3 MB, less than 69.31% of Python3 online submissions for Serialize and Deserialize BST.
"""