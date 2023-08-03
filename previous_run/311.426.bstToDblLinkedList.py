"""
https://leetcode.com/problems/convert-binary-search-tree-to-sorted-doubly-linked-list/?envType=study-plan&id=programming-skills-iii


it looks like a in-order traversal
yes.. with extra memory it is trivial

but in place...

this is actually next node.. precedesor or next node
morris traversal

"""


from typing import Optional


class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def treeToDoublyList(self, root: 'Optional[Node]') -> 'Optional[Node]':
        dummy = Node(0, None, None)
        predcesor = dummy

        curr = root
        while curr:
            if curr.left is None:
                predcesor.right = curr
                curr.left = predcesor
                predcesor = curr
                curr = curr.right
            else:
                # Find the previous (prev) of currs
                prev = curr.left
                # if the prev.right is curr
                # thou shall not follow it thru any more
                while(prev.right is not None and prev.right != curr):
                    prev = prev.right

                # Make curr as right child of its prev
                if(prev.right is None):
                    prev.right = curr
                    curr = curr.left
                # fix the right child of prev
                else:
                    predcesor.right = curr
                    curr.left = predcesor
                    predcesor = curr
                    curr = curr.right
        dummy.right.left, predcesor.right = predcesor, dummy.right
        return dummy.right


class Solution:
    def treeToDoublyList(self, root: 'Optional[Node]') -> 'Optional[Node]':
        dummy = Node(0, None, None)
        predcesor = dummy

        curr = root
        stack = []
        while stack or curr:
            while curr:
                stack.append(curr)
                curr = curr.left

            # one node at a time
            node = stack.pop()
            predcesor.right, node.left, predcesor = node, predcesor, node
            curr = node.right

        dummy.right.left, predcesor.right = predcesor, dummy.right
        return dummy.right


class Solution:
    def treeToDoublyList(self, root: 'Node') -> 'Node':

        # inorder traversal sol - recursion
        if not root:
            return None

        dummy = Node(-1)
        prev = dummy

        def inorder(root):
            nonlocal prev
            if not root:
                return
            inorder(root.left)
            # okay.. this link happens when outputting the data
            # when outputting? the middle place of the in-order traversal..
            # it is the same as stack-based in-order
            # or morris's traversal (it has two places to output data: 1.. reach the left end; 2.. going back left but circle to itself...)
            # or classical traversal
            # one node at a time

            prev.right, root.left, prev = root, prev, root
            inorder(root.right)

        inorder(root)
        dummy.right.left, prev.right = prev, dummy.right
        return dummy.right


if __name__ == "__main__":
    node = Node(2, Node(1), Node(3))
    Solution().treeToDoublyList(node)
