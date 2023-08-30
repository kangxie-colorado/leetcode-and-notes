"""
not much thought

thinking I can sort it by height, I place the highest person first
(7,0) (7,1) I can only place in one order, which is (7,0) (7,1)

then for next height, (6,1)..
apparently I cannot place before (7,0), then it won't be having 1 higher or eqaul, cannot place is behind (7,1)
then it cannot be 1 (but 2) higher so it has to be (7,0) (6,1) (7,1)

then (5,0) it can only be to the front
(5,1) it can only be to the 2nd after (7,0)

the element movement is troublesome but at most O(n**2) ...

not much better way I can think 
"""

from typing import List

class LinkNode:
    def __init__(self, val, next=None) -> None:
        self.val = val
        self.next = next 

class Solution:
    def reconstructQueue(self, people: List[List[int]]) -> List[List[int]]:
        
        people.sort(key=lambda x: (-x[0], x[1]))
        
        head = LinkNode(people[0])
        for p in people[1:]:
            h,n = p[0], p[1]
            if p[1] == 0:
                newHead = LinkNode(p, head)
                head = newHead
                continue

            # find a pos that has n people in the front that is higher or eqaul to h
            prev = head
            next = head.next
            while n>1:
                prev = prev.next
                next = next.next
                n-=1
            prev.next = LinkNode(p,next)

        res = []
        while head:
            res.append(head.val)
            head = head.next
        return res
                
            
                
                





if __name__ == '__main__':
    s = Solution()
    print(s.reconstructQueue(people = [[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]))
    print(s.reconstructQueue(people = [[6,0],[5,0],[4,0],[3,2],[2,2],[1,4]]))