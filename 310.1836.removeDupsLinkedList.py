"""
https://leetcode.com/problems/remove-duplicates-from-an-unsorted-linked-list/?envType=study-plan&id=programming-skills-iii

need to store them..
front and back nodes. 
"""


from collections import defaultdict
from utils import ListNode


class Solution:
    def deleteDuplicatesUnsorted(self, head: ListNode) -> ListNode:
        dummy = ListNode(0, head)
        m = defaultdict(int)
        while head:
            m[head.val] += 1
            head = head.next

        head = dummy.next
        prev = dummy
        while head:
            if m[head.val] > 1:
                prev.next = head.next
            else:
                prev = head
            head = head.next

        return dummy.next
