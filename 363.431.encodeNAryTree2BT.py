"""
https://leetcode.com/problems/encode-n-ary-tree-to-binary-tree/?envType=study-plan&id=programming-skills-iii


I didn't have any idea how to do it
but this problem has a very high acceptance rate

it should not be very difficult
read someone says subtree to left and right sibling to right then I see

let me give a try
"""


# Definition for a Node.
from collections import deque
from typing import Optional


class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children



# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None



class Codec:
    # Encodes an n-ary tree to a binary tree.
    def encode(self, root: 'Optional[Node]') -> Optional[TreeNode]:
        if not root:
            return None

        def helper(siblings):
            if not siblings:
                return None

            node = siblings[0]
            btNode = TreeNode(node.val)
            btNode.left = helper(node.children)
            btNode.right = helper(siblings[1:])

            return btNode 
        return helper([root])

	# Decodes your binary tree to an n-ary tree.
    def decode(self, data: Optional[TreeNode]) -> 'Optional[Node]':
        if not data:
            return None
        
        def helper(root):
            if root is None:
                return []
            btRightNodes = []
            curr = root
            while curr:
                btRightNodes.append(curr)
                curr = curr.right 
            
            nodes = []
            for btNode in btRightNodes:
                node = Node(btNode.val)
                node.children = helper(btNode.left)
                nodes.append(node)
            
            return nodes
        return helper(data)[0]
"""
Runtime: 98 ms, faster than 66.48% of Python3 online submissions for Encode N-ary Tree to Binary Tree.
Memory Usage: 22.5 MB, less than 6.59% of Python3 online submissions for Encode N-ary Tree to Binary Tree.
"""