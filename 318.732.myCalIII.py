"""
https://leetcode.com/problems/my-calendar-iii/

this tree only return overlapping count
so only need the update function 
"""


from sortedcontainers import SortedDict
class SegmentTreeNode:
    def __init__(self, start=0, end=0, count=0, left=None, right=None) -> None:
        self.start = start
        self.end = end

        self.count = count
        self.left = left
        self.right = right
    


def printSegmentTree(node):

    q = [(node, 0, '^')]
    idx = 1
    pIdx = 0
    while q:
        count = len(q)
        level = ""
        while count:
            node, pIdx, lr = q[0]
            q = q[1:]
            if node:
                level = f"{level}  {pIdx}-{lr}-{idx}:[{node.start},{node.end},{node.count}]"
                if node.left:
                    q.append((node.left, idx, 'l'))
                if node.right:
                    q.append((node.right, idx, 'r'))
            else: 
                level = f"{level}  {idx}-None"
            count-=1
            idx+=1

        print(level)
    print()
        

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

# WARNING: this version has that push-down loss 
class MyCalendarThree:

    def __init__(self):
        self.root = SegmentTreeNode()
        self.max = 0

    def book(self, start: int, end: int) -> int:
        def update(root, start, end):
            if start >= end:
                # it is none of your business
                # or it is an empty range.. no need to build a node for empty range
                return root
            if root is None:
                # this is a new interval
                self.max = max(self.max, 1)
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
                self.max = max(self.max, root.count)

                root.left = update(root.left, a, b)
                root.right = update(root.right, c, d)

            return root

        update(self.root, start, end)
        return self.max



# trying to fix that push down loss
# firstly, trying to use the old value after it gets updated
# a so bad logical error
class MyCalendarThree:
    def __init__(self):
        self.root = SegmentTreeNode()
        self.max = 0

    def book(self, start: int, end: int) -> int:
        pushDownMap = {}
        def update(root, start, end):
            if start >= end:
                # it is none of your business
                # or it is an empty range.. no need to build a node for empty range
                return root
            if root is None:
                # this is a new interval
                count = 1
                if (start,end) in pushDownMap:
                    count = pushDownMap[(start, end)]
                    
                self.max = max(self.max, count)
                return SegmentTreeNode(start, end, count)

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
                
                if root.start <= a and b <= root.end:
                    pushDownMap[(a, b)] = root.count

                if root.start <= c and d <= root.end:
                    pushDownMap[(c, d)] = root.count

                root.start = b
                root.end = c
                root.count += 1
                self.max = max(self.max, root.count)


                root.left = update(root.left, a, b)
                root.right = update(root.right, c, d)

            return root

        update(self.root, start, end)
        return self.max


"""
Runtime: 342 ms, faster than 96.32% of Python3 online submissions for My Calendar III.
Memory Usage: 15.4 MB, less than 18.61% of Python3 online submissions for My Calendar III.

okay.. so agnoy comes from 
                if root.start <= a and b <= root.end:
                    pushDownMap[(a, b)] = root.count

                if root.start <= c and d <= root.end:
                    pushDownMap[(c, d)] = root.count

                root.start = b
                root.end = c
                root.count += 1
                self.max = max(self.max, root.count)

I wrote it as beow -- update root before I need its old value
                root.start = b
                root.end = c
                root.count += 1
                self.max = max(self.max, root.count)

                if root.start <= a and b <= root.end:
                    pushDownMap[(a, b)] = root.count

                if root.start <= c and d <= root.end:
                    pushDownMap[(c, d)] = root.count

gives me idea maybe I can still do that push down
"""


class MyCalendarThree:
    def __init__(self):
        self.root = SegmentTreeNode()
        self.max = 0

    def book(self, start: int, end: int) -> int:
        def update(root, start, end, pushDownCount):
            # pushDownCount is how many should the split child inherits 
            # edge case being if it is total subset of root.. it must inherit root.count
            # e.g. 10,30,3 with incoming 5,20
            # it will become 1-10, which is new 1
            # also 1-20, which is 3+1 = 4
            # also 20-30, which is? absolutely not 1.. it should be 3 

            if start >= end:
                # it is none of your business
                # or it is an empty range.. no need to build a node for empty range
                return root
            if root is None:
                # this is a new interval
                self.max = max(self.max, pushDownCount)
                return SegmentTreeNode(start, end, pushDownCount)

            if root.end <= start:
                root.right = update(root.right, start, end, pushDownCount)

            elif root.start >= end:
                root.left = update(root.left, start, end, pushDownCount)
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

                leftPushDown=rightPushDown=1
                if root.start <= a and b <= root.end:
                    leftPushDown = root.count 
                if root.start <= c and d <= root.end:
                    rightPushDown = root.count

                root.start = b
                root.end = c
                root.count += 1
                self.max = max(self.max, root.count)

                root.left = update(root.left, a, b, leftPushDown)
                root.right = update(root.right, c, d, rightPushDown)

            return root

        update(self.root, start, end,1)
        return self.max


"""
Runtime: 311 ms, faster than 96.75% of Python3 online submissions for My Calendar III.
Memory Usage: 14.6 MB, less than 55.41% of Python3 online submissions for My Calendar III.

okay... it is still right...
I am still not familiar with this enough
"""


class MyCalendarThree:

    def __init__(self):
        self.sMap = SortedDict()

    def book(self, startTime: int, endTime: int) -> int:
        if startTime not in self.sMap:
            self.sMap[startTime] = 0
        self.sMap[startTime] += 1

        if endTime not in self.sMap:
            self.sMap[endTime] = 0
        self.sMap[endTime] -= 1

        # curr will meet +1, -1, so it kind of reflect the curr most bookings
        # res will only be the max bookings..
        # genius idea ... 
        res = curr = 0
        for time, count in self.sMap.items():
            curr += count
            res = max(res, curr)

        return res

if __name__ == '__main__':
    # op = ["book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book","book"]
    # # args = [[97,100],[51,65],[27,46],[90,100],[20,32],[15,28],[60,73],[77,91],[67,85],[58,72],[74,93],[73,83],[71,87],[97,100],[14,31],[26,37],[66,76],[52,67],[24,43],[6,23],[94,100],[33,44],[30,46],[6,20],[71,87],[49,59],[38,55],[4,17],[46,61],[13,31],[94,100],[47,65],[9,25],[4,20],[2,17],[28,42],[26,38],[72,83],[43,61],[18,35]]
    # args = [[27, 46], [20, 32], [15, 28], [14, 31], [26, 37], [24, 43], [6, 23], [
    #     33, 44], [30, 46], [6, 20], [4, 17], [4, 20], [2, 17], [28, 42], [26, 38]]

    # this input shows something wrong with logic
    args = [[27, 46], [20, 32], [15, 28]]
    mycal3 = MyCalendarThree()
    for arg in args:
        print(mycal3.book(*arg), arg)
        printSegmentTree(mycal3.root.right)
    """
okay.. above reveals what is wrong 
1 [27, 46]
    0-^-1:[27,46,1]

2 [20, 32]
  0-^-1:[27,32,2]
  1-l-2:[20,27,1]  1-r-3:[32,46,1]

3 [15, 28]
  0-^-1:[27,28,3]
  1-l-2:[20,27,2]  1-r-3:[32,46,1]
  2-l-4:[15,20,1]  3-l-5:[28,32,1]
                            ^^ here 28-32 should have appeared twice now already

    the reason is maybe here
    when 15-28 + 27-32.. it pushes 28-32 to right.. 
    it should bear its 2 to start.. not 1 to start.. 
    let me see where to make the fix

    to keep the scene I'll copy a new class

    """

    args = [[27, 46], [20, 32], [15, 28], [14, 31], [26, 37], [24, 43], [6, 23], [
        33, 44], [30, 46], [6, 20], [4, 17], [4, 20], [2, 17], [28, 42], [26, 38]]

    # this input shows something wrong with logic
    mycal3 = MyCalendarThree()
    for arg in args:
        print(mycal3.book(*arg), arg)
        printSegmentTree(mycal3.root.right)
