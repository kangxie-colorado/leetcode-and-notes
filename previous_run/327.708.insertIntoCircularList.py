"""
https://leetcode.com/problems/insert-into-a-sorted-circular-linked-list/?envType=study-plan&id=programming-skills-iii


didn't feel this is super complciated

because it is circular list
so if there are more than 2 values.. find the mid place?
but 1,2 adding 3... not like that

but if there is only 1 or 0 values.. then any place can be 

if it is smaller than or bigger than any values.. then it must be inserted between the smallest and biggest nodes


"""


from typing import Optional


class Node:
    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next

class Solution:
    def insert(self, head: 'Optional[Node]', insertVal: int) -> 'Node':
        if not head:
            newNode = Node(insertVal)
            newNode.next = newNode
            return newNode

        if head.next == head:
            newNode = Node(insertVal)
            newNode.next = head
            head.next = newNode
            return head

        maxVal, maxNode = head.val, head

        prev = head
        curr = head.next
        while curr != head:
            if prev.val <= insertVal <= curr.val:
                newNode = Node(insertVal)
                prev.next = newNode
                newNode.next = curr
                return head
            
            if curr.val > maxVal:
                maxVal, maxNode = curr.val, curr


            prev = prev.next
            curr = curr.next
        
        # need following because the last step is not walked yet 
        # after this step.. it walks the full circle
        if prev.val <= insertVal <= curr.val:
            newNode = Node(insertVal)
            prev.next = newNode
            newNode.next = curr
            return head

        # for insertval>maxVal it goes behind the last maxNode
        # for insertval<minVal, surprisinly it also goes behind the last MaxNode
        # if the current maxNode is not the last or it is all node's vals
        # go to the last or a circle
        stop = maxNode
        while maxNode.next.val == maxVal and maxNode.next != stop:
            maxNode = maxNode.next
        newNode = Node(insertVal, maxNode.next)
        maxNode.next = newNode

        return head

"""
Runtime: 41 ms, faster than 86.44% of Python3 online submissions for Insert into a Sorted Circular Linked List.
Memory Usage: 14.8 MB, less than 86.28% of Python3 online submissions for Insert into a Sorted Circular Linked List.
"""


class Solution:
    def insert(self, head: 'Optional[Node]', insertVal: int) -> 'Node':
        newNode = Node(insertVal)
        if not head:
            newNode.next = newNode
            return newNode

        if head.next == head:
            newNode.next = head
            head.next = newNode
            return head

        maxVal, maxNode = head.val, head

        prev = head
        curr = head.next
        atStart = True
        while atStart or curr != head.next:
            atStart = False
            if prev.val <= insertVal <= curr.val:
                newNode = Node(insertVal)
                prev.next = newNode
                newNode.next = curr
                return head

            if curr.val > maxVal:
                maxVal, maxNode = curr.val, curr

            prev = prev.next
            curr = curr.next

        # for insertval>maxVal it goes behind the last maxNode
        # for insertval<minVal, surprisinly it also goes behind the last MaxNode
        # if the current maxNode is not the last or it is all node's vals
        # go to the last or a circle
        stop = maxNode
        while maxNode.next.val == maxVal and maxNode.next != stop:
            maxNode = maxNode.next
        newNode = Node(insertVal, maxNode.next)
        maxNode.next = newNode

        return head


"""
Runtime: 41 ms, faster than 86.44% of Python3 online submissions for Insert into a Sorted Circular Linked List.
Memory Usage: 14.8 MB, less than 86.28% of Python3 online submissions for Insert into a Sorted Circular Linked List.
"""