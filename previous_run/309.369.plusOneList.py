"""
https://leetcode.com/problems/plus-one-linked-list/?envType=study-plan&id=programming-skills-iii

okay.. it is a linked list.. 
it is slightly tricky

if it is an array.. I just reverse it and it becomes trivial
but for a linked list

I can just do that after dfs return

"""
from utils import ListNode


class Solution:
    def plusOne(self, head: ListNode) -> ListNode:
        dummy = ListNode(0, head)

        # return the carry over -- just think there is a carry 1
        def helper(node):
            if node is None:
                return 1

            num = helper(node.next) + node.val
            node.val = num % 10
            return num // 10

        helper(dummy)
        if dummy.val == 1:
            return dummy
        return dummy.next


class Solution:
    def plusOne(self, head: ListNode) -> ListNode:
        dummy = ListNode(0, head)
        stack = [dummy]

        while head:
            stack.append(head)
            head = head.next

        carry = 1
        while stack:
            node = stack.pop()
            num = node.val + carry
            node.val = num % 10
            carry = num//10

        if dummy.val == 1:
            return dummy
        return dummy.next
