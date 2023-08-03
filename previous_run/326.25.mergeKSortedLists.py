"""
https://leetcode.com/problems/merge-k-sorted-lists/?envType=study-plan&id=programming-skills-iii

apparently this uses heap
but why did I do something like this? 

class ComparbleListNode(ListNode):
    def __init__(self, val=0, next=None):
        super().__init__(val, next)
    def __lt__(self, other):
        return self.val < other.val

ah.. it is for this reason

TypeError: '<' not supported between instances of 'ListNode' and 'ListNode'
    heapq.heappush(h, (l.val, l))
Line 11 in mergeKLists (Solution.py)
    ret = Solution().mergeKLists(param_1)
Line 40 in _driver (Solution.py)
    _driver()
Line 51 in <module> (Solution.py)

okay... then I just need to use the node itself? with this datastructure 
"""


from ast import List
import heapq
from typing import Optional
from utils import ListNode


class ComparbleListNode(ListNode):
    def __init__(self, node):
        super().__init__(node.val, node.next)
        self.node = node

    def __lt__(self, other):
        return self.node.val < other.node.val


class Solution:

    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        dummy = ListNode(0)
        tail = dummy
        h = []  # (val, node)

        for l in lists:
            if l:
                heapq.heappush(h, ComparbleListNode(l))

        while h:
            node = heapq.heappop(h)
            tail.next = node.node
            tail = tail.next

            if node.node.next:
                heapq.heappush(h, ComparbleListNode(node.node.next))

        return dummy.next
