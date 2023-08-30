"""
did this before but not so clearly remembered right now
maybe reverse and interleave
"""

# Definition for singly-linked list.
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        slow=fast=ListNode(0,head)
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next 
        
        def reverseList(node):
            stack = []
            while node:
                stack.append(node)
                node = node.next 
            
            dummy = ListNode()
            next = dummy
            while stack:
                node = stack.pop()
                node.next = None 
                next.next = node 
                next = node 
            
            return dummy.next
        
        def interLeaveList(head1, head2):
            dummy = ListNode()
            next = dummy
            while head1 and head2:
                nextHead1 = head1.next 
                nextHead2 = head2.next 
                head1.next = head2.next = None

                next.next = head1
                next.next.next = head2 
                next = head2 

                head1 = nextHead1
                head2 = nextHead2
            
            next.next = head1 or head2 
            return dummy.next
        
        secHalf = reverseList(slow.next)
        slow.next = None

        interLeaveList(head, secHalf)

if __name__ == '__main__':
    l = ListNode(1, ListNode(2, ListNode(3, ListNode(4))))
    Solution().reorderList(l)

    print(l)