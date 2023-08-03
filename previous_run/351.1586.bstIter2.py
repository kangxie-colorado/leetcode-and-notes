"""
https://leetcode.com/problems/binary-search-tree-iterator-ii/

thinking that stack based inorder traversal
going left until not anymore
pop up.. then going to its right (left... then...)

so hasNext is stack is not empty
next, pop up the stack top, then put next node on the top 
    - it could be it is the min node, then next node in the stack will become natrually the next
    - if it has a right node.. then stack that right.left.left...left like earlier
hasPrev, is pointer is not the guardian
prev, prev will be saved in a stack.. return it and put it back to stack 
    - the idea of operating prev like another stack complicates things quite a lot
    - so I revise it to be a plain list.. for all the popped values
    - just saved it in a plain list and maintain the cursor idx to operate

"""

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


from typing import Optional

from utils import TreeNode


class BSTIterator:

    def __init__(self, root: Optional[TreeNode]):
        self.nextStack = []
        # for simplicity, just record all the visited values in a list
        # popped[-1] is the biggest node that has been visited
        # use self.cursor to record the movement along this list
        self.popped = [] 
        self.cursor = -1

        curr = root 
        while curr:
            self.nextStack.append(curr)
            curr = curr.left


    def hasNext(self) -> bool:
        return self.cursor<len(self.popped)-1 or len(self.nextStack)

    def next(self) -> int:
        self.cursor += 1
        if self.cursor < len(self.popped):
            return self.popped[self.cursor].val

        node = self.nextStack.pop()
        self.popped.append(node)
        
        # now, find the next successor 
        curr = node.right
        # this naturally takes care of no-right-child scenario 
        while curr:
            self.nextStack.append(curr)
            curr = curr.left 
        
        return node.val

    def hasPrev(self) -> bool:
        return self.cursor>0

    def prev(self) -> int:
        self.cursor -= 1
        node = self.popped[self.cursor]
    
        return node.val

"""
Runtime: 454 ms, faster than 95.45% of Python3 online submissions for Binary Search Tree Iterator II.
Memory Usage: 46.3 MB, less than 36.36% of Python3 online submissions for Binary Search Tree Iterator II.
"""