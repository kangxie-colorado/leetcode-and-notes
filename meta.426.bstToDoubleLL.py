class Node:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def treeToDoublyList(self, root: 'Node') -> 'Node':
        if not root:
            return None

        head = root 
        while head.left:
            head = head.left 
        tail = root 
        while tail.right:
            tail = tail.right 

        
        def f(root):
            if not root:
                return None,None
            
            lHead, lTail = f(root.left)
            rHead, rTail = f(root.right)
            
            root.left = lTail
            if lTail:
                lTail.right = root
                
            root.right = rHead
            if rHead:
                rHead.left = root
            
            return lHead or root, rTail or root
        
        f(root)
        head.left = tail
        tail.right = head 

        return head


"""
because this is BST
dumb way is to turn it into an array.. 

if you cannot make an extra array
then just in-order traversal.. 


"""

class Solution:
    def treeToDoublyList(self, root: 'Node') -> 'Node':
        if not root:
            return None
        
        dummy = Node(-1)
        tail = dummy
        
        def inorder(root):
            if not root:
                return 
            
            inorder(root.left)
            # now at my level, process root
            nonlocal tail
            tail.right, root.left, tail = root, tail, root
            inorder(root.right)
        
        inorder(root)
        head = dummy.right
        head.left, tail.right = tail, head
        return head