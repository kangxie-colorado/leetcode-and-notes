"""
https://leetcode.com/problems/my-calendar-ii/

okay.. this segment tree is a evasive force
I cannot get to grasp it

let me just tranlaste someone's code and debug and see

"""


from sortedcontainers import SortedDict
class SegmentTreeNode:
    def __init__(self, start=0, end=0, count=0, left=None,right=None) -> None:
        self.start = start
        self.end = end

        self.count = count
        self.left = left
        self.right = right

# don't think start,end as two separate things
# it is the vals here.. 
# I confuse it as a range 
# I came from that dicrete examples.. that l,r is truly a range (afterall, that is range sum exmaple)
def query(root, start, end):
    if start >= end or root is None:
        # root is None meaning there is no interval existing yet
        # it can happen when it walks off the edge into the void
        # e..g root is now 10,30... on incoming 50,60.. it walks to right and its a void

        return 0
    
    if root.start >= end:
        return query(root.left, start, end)
    
    if root.end <= start:
        return query(root.right, start, end)

    # the max overlapping among root range, left range and right range
    return max(root.count, query(root.left, start, end), query(root.right, start, end))


def update(root, start, end):
    if start>=end:
        # it is none of your business 
        # or it is an empty range.. no need to build a node for empty range
        return root
    if root is None:
        # this is a new interval 
        return SegmentTreeNode(start, end, 1)

    if root.end <= start:
        root.right = update(root.right, start, end)
    
    elif root.start >= end:
        root.left = update(root.left, start, end)
    else:
        # span both left/right 
        # e.g. [10,30] with incoming [15,25]
        # it will split int [10,15].. [15. 25].. and [25,30]
        # the mid range(b,c) will have one more count here +=1
        # the left/right ranges (a,b) and (c,d) will form new ranges.. and could populate downwards...
        a = min(start, root.start)
        b = max(start, root.start)
        c = min(end, root.end)
        d = max(end, root.end)

        root.start = b
        root.end = c
        root.count += 1

        root.left = update(root.left, a,b)
        root.right = update(root.right, c,d)
    
    return root



class MyCalendarTwo:

    def __init__(self):
        self.root = SegmentTreeNode()

    def book(self, start: int, end: int) -> bool:
        if query(self.root, start, end) >= 2:
            return False
        
        self.root = update(self.root, start, end)
        return True

"""
okay.. 
update didn't update root's start/end.. 
so root starts with 0,0
after 10,20
the right tree becomes 10,20, but root is still 0,0????

okay.. maybe this root is misplaced.. 
there is nothing that can go below 0,0

the new branches will open under 10,20... and I think that is the case
and the 10,20 is actually the effective root

the 0,0 is the dummy.. 
anyway.. not matter 

okay.. the node 10,20 still doesn't change at all
so indeed this is not a range sum problem but a overlapping 

actually it will change
here
        root.start = b
        root.end = c
        root.count += 1

root will become the overlapping and the left/right intervals got pushed down
"""


class MyCalendarTwo:

    def __init__(self):
        self.sMap = SortedDict()
    def book(self, start: int, end: int) -> bool:
        # I thought save the plus+1/minus-1 unless its necessary
        # but it messes things up
        # cannot save it... and it is not expensive
        # this kind of works in the way it has to be
        # cannot do half of it
        # I thought I can add start only.. and if start is overlap..
        # i back out.. and I don't need to change end
        # but it changes the internal state and corrupted big time...

        if start not in self.sMap:
            self.sMap[start] = 0
        self.sMap[start] += 1

        if end not in self.sMap:
            self.sMap[end] = 0
        self.sMap[end] -= 1

        curr = 0
        for _,count in self.sMap.items():
            curr += count
            if curr > 2:
                self.sMap[start] -= 1
                self.sMap[end] += 1
                return False

        return True
                
            

        

if __name__ == '__main__':
    # mycal = MyCalendarTwo()
    # print(mycal.book(10,20))
    # print(mycal.book(50,60))
    # print(mycal.book(10,40))
    # print(mycal.book(5,15))
    # print(mycal.book(5,10))
    # print(mycal.book(25,55))

    
    args = [[24,40],[43,50],[27,43],[5,21],[30,40],[14,29],[3,19],[3,14],[25,39],[6,19]]
    mycal = MyCalendarTwo()
    for i, arg in enumerate(args):
        print(mycal.book(*arg))