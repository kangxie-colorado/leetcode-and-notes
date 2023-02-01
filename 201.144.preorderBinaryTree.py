"""
https://leetcode.com/problems/binary-tree-preorder-traversal/

hmm.. not that simple

need to use stack and append right before left
this way, it can do the right order..
"""

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


from typing import List, Optional

from utils import TreeNode


class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        s = [root]
        res = []
        while len(s):
            node = s[-1]
            s = s[:len(s)-1]
            if node is None:
                continue
            res.append(node.val)

            s.append(node.right)
            s.append(node.left)
        return res


"""
Runtime: 52 ms, faster than 38.95% of Python3 online submissions for Binary Tree Preorder Traversal.
Memory Usage: 13.9 MB, less than 60.05% of Python3 online submissions for Binary Tree Preorder Traversal.
"""


class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        stack = []
        curr = root
        res = []
        while curr or stack:
            while curr:
                res.append(curr.val)
                stack.append(curr)
                curr = curr.left

            node = stack.pop()
            curr = node.right

        return res


"""
Runtime: 33 ms, faster than 90.92% of Python3 online submissions for Binary Tree Preorder Traversal.
Memory Usage: 14 MB, less than 13.06% of Python3 online submissions for Binary Tree Preorder Traversal.

1/29/2023: revisit this again
the first solution is easy to understand: process current-node,  push to stack right then left
and then pop and repeat

the second solution is interesting but same idea
process all way thru the left then from the leaf. pop a node and go to right
it could be none.. and that is implicitly skipped
I also came up with something else today but a bit more ugly
"""


class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        stack = []
        curr = root
        res = []

        while curr or stack:
            if curr:
                res.append(curr.val)
                stack.append(curr.right)
                if curr.left:
                    curr = curr.left
                else:
                    curr = stack.pop()
            else:
                curr = stack.pop()

        return res


"""
Runtime: 30 ms, faster than 78.10% of Python3 online submissions for Binary Tree Preorder Traversal.
Memory Usage: 14 MB, less than 7.87% of Python3 online submissions for Binary Tree Preorder Traversal.

I tried to do more control
if curr is not none, routine:
        append value
        push right
        exhaust left , then back to right
if curr is already none,
    pop to switch to right..

messy..
        
"""

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        stack = []
        res = []
        curr = root

        while curr or stack:
            # exhaust left first
            while curr:
                res.append(curr.val)
                stack.append(curr)
                curr = curr.left

            # switch to right
            curr = stack.pop().right

        return res


class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        stack = [root]
        res = []

        while stack:
            node = stack.pop()
            if node:
                res.append(node.val)

                stack.append(node.right)
                stack.append(node.left)

        return res


class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        stack = []
        res = []
        curr = root

        while curr or stack:
            # exhaust left first
            while curr:
                res.append(curr.val)
                stack.append(curr.right)
                curr = curr.left

            # switch to right
            curr = stack.pop()

        return res
