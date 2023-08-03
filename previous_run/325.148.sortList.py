"""
https://leetcode.com/problems/sort-list/?envType=study-plan&id=programming-skills-iii

I think this is a merge sort?

"""

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


from typing import Optional

from utils import ListNode


class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:

        def sort(head):
            if not head or not head.next:
                return head

            dummy = ListNode(0, head)
            slow = dummy.next
            fast = dummy.next.next

            while fast and fast.next:
                slow = slow.next 
                fast = fast.next.next 
            
            rightHead = slow.next 
            leftHead = dummy.next
            slow.next = None 

            leftHead = sort(leftHead)
            rightHead = sort(rightHead)

            tail = dummy
            while leftHead and rightHead:
                if leftHead.val < rightHead.val:
                    tail.next = leftHead
                    leftHead = leftHead.next
                else:
                    tail.next = rightHead
                    rightHead = rightHead.next
                
                tail = tail.next
            
            tail.next = rightHead or leftHead
            return dummy.next
        
        return sort(head)

"""
Runtime: 685 ms, faster than 81.97% of Python3 online submissions for Sort List.
Memory Usage: 36.5 MB, less than 54.02% of Python3 online submissions for Sort List.

okay.. this is recursion so not constant space.
that constant space I don't want to force myself to unerstand and write
but after checking others code... 

it is genius idea.. at least let me write it by translation 
"""


class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head

        # get length
        curr = head
        l = 0
        while curr:
            l += 1
            curr = curr.next

        dummy = ListNode(0, head)

        # split function splits n nodes out of the list
        # the main will call two splits
        # then merge them and record the tail (it will used to chain up furthre split/merge)
        # n=1.. it split 1/2 node. merge; then 3/4 node merge.. then n-1/n node, merge
        # the bookkeeping in the driver code is a must 

        def split(head, n):
            # watch out the n=1, meaning I only need head itself
            # so n should be >1 (ending position)
            # also notice here I am changing head.. but this arg is passed as a copy
            # so outside.. is not changed.
            # a copy of pointer.. but the orig pointer is not changed... a little confuse
            while n-1 and head:
                head = head.next
                n -= 1

            if not head:
                return None

            rightSide = head.next
            head.next = None
            return rightSide

        def merge(l1, l2, head):
            curr = head
            while l1 and l2:
                if l1.val < l2.val:
                    curr.next = l1
                    l1 = l1.next
                else:
                    curr.next = l2
                    l2 = l2.next
                curr = curr.next

            curr.next = l1 or l2
            while curr.next:
                curr = curr.next
            return curr

        step = 1
        while step < l:
            curr = dummy.next
            tail = dummy
            while curr:
                left = curr
                # this split step nodes following left it will be lead by left
                # right as the return value is the node that is not splitted 
                # okay.. this return right.. as the left-over list part
                # but actually the left pointer is being modified to form the left-side list
                # after 
                right = split(left, step)
                # this is bookkeeping because the list is gonna change state after merge
                # so precompute the next split point 
                # yeah... this idea is hard to come up
                # ah.. this is not only the bookkeeping
                # it is also the 2nd split.. then bookkeeping 
                curr = split(right, step)
                tail = merge(left, right, tail)

            step *= 2

        return dummy.next

"""
Runtime: 1005 ms, faster than 57.02% of Python3 online submissions for Sort List.
Memory Usage: 36.5 MB, less than 28.06% of Python3 online submissions for Sort List.
"""

def move_point(p):
    p = p.next 
    print(p.val)


if __name__ == '__main__':
    s = Solution()
    # l1 = ListNode(4,ListNode(2, ListNode(1, ListNode(3))))
    # s.sortList(l1)
    l2 = ListNode(-1, ListNode(5, ListNode(3, ListNode(4, ListNode(0)))))

    # just to verify the copy of pointer..
    print(l2.val)  # print -1
    move_point(l2)  # print 5
    print(l2.val)  # print -1 still


    s.sortList(l2)


    
                





            

