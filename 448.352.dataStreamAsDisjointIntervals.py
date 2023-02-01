"""
https://leetcode.com/problems/data-stream-as-disjoint-intervals/?envType=study-plan&id=graph-ii

huh? what is the problem asking?
ah.. basically return the connected parts as interval 1,2,3,4 -> [1,4]

union find - 
    use a set to record number 
    union with its prev/next number if they are in the set 

not sure if it can pass but at least to start me
"""


from bisect import bisect_left
from collections import defaultdict
from typing import List

from sortedcontainers import SortedList


class SummaryRanges:

    def __init__(self):
        self.values = set()
        self.roots = {}
        self.groups = {}

    def find(self, x):
        self.roots.setdefault(x,x)
        if self.roots[x] != x:
            self.roots[x] = self.find(self.roots[x])
        return self.roots[x]
    
    def union(self, x,y):
        self.roots[self.find(x)] = self.roots[self.find(y)]
    
    def addNum(self, value: int) -> None:
        self.values.add(value)

        self.union(value, value)
        if value - 1 in self.values:
            self.union(value, value-1)
        if value + 1 in self.values:
            self.union(value, value+1)

    def getIntervals(self) -> List[List[int]]:
        groups = defaultdict(set)
        for n in self.roots:
            r = self.find(n)
            groups[r].add(n)
        
        return sorted([ [ min(grp), max(grp) ] for grp in groups.values()])

"""
Runtime: 2060 ms, faster than 6.71% of Python3 online submissions for Data Stream as Disjoint Intervals.
Memory Usage: 19.1 MB, less than 25.17% of Python3 online submissions for Data Stream as Disjoint Intervals.

okay.,., let me try optimize 
notice the scan interval happens every time
but it may not need to 

With every addNum, it at most impacts two intervals.. the prev/next if they exists
I could merge the groups accordingly
"""


class SummaryRanges_total_mess:

    def __init__(self):
        self.values = set()
        self.roots = {}
        self.groups = {}

    def find(self, x):
        self.roots.setdefault(x, x)
        if self.roots[x] != x:
            self.roots[x] = self.find(self.roots[x])
        return self.roots[x]

    def union(self, x, y):
        r1 = self.find(x)
        r2 = self.find(y)
        if r1<r2:
            self.roots[r2] = self.roots[r1]
        else:
            self.roots[r1] = self.roots[r2]

    def addNum(self, value: int) -> None:
        self.values.add(value)

        self.union(value, value)
        if value - 1 in self.values:
            root = self.find(value-1)
            s,_ = self.groups[root]

            self.union(value, value-1)
            self.groups[root] = (s,value)
        else:
            # this is to make sure self.roots[x] = x at least
            # this 
            
            self.groups[value] = [value, value]

        if value + 1 in self.values:
            root2 = self.find(value + 1)
            _,e = self.groups[root2]

            root1 = self.find(value)
            s, _ = self.groups[root1]

            self.union(value, value+1)
            self.groups[root1] = (s, e)

            self.groups.pop(root2)

        

    def getIntervals(self) -> List[List[int]]:
        return sorted([[min(grp), max(grp)] for grp in self.groups.values()])

""""
okay.. because the root can change.. 
it is very messed up

actually this doesn't need to use union find to solve
just keep the intervals in an ordered list.. merge them accordingly 

but the union find solution is interesting to write as well
"""


class SummaryRanges:

    def __init__(self):
        self.intervals = SortedList()
        self.values = set()

    def addNum(self, value: int) -> None:
        
        if value in self.values:
            return
        self.values.add(value)

        if not self.intervals:
            self.intervals.add([value, value])
            return 

        idx = self.intervals.bisect_left([value, value])
        newInterval = [value,value]
        
        if idx < len(self.intervals) and self.intervals[idx][0]-1 == value:
            # merge right
            # I can delete right side and it doesn't impact the left side, right?
            rightS, rightE = self.intervals[idx]
            newInterval[1] = rightE
            self.intervals.remove([rightS, rightE])


        if idx>0 and self.intervals[idx-1][1]+1==value:
            # merge left
            leftS, leftE = self.intervals[idx-1]    
            newInterval[0] = leftS
            self.intervals.remove([leftS, leftE])
            
        self.intervals.add(newInterval)
        

    def getIntervals(self) -> List[List[int]]:

        return list(self.intervals)


"""
Runtime: 167 ms, faster than 79.53% of Python3 online submissions for Data Stream as Disjoint Intervals.
Memory Usage: 19.4 MB, less than 14.09% of Python3 online submissions for Data Stream as Disjoint Intervals.

I remember that slice operation.. 
maybe it can be simplified -- but perhaps sortedlist doesn't support that
if so, I can just use ordinary list
"""


class SummaryRanges:

    def __init__(self):
        self.intervals = []
        self.values = set()

    def addNum(self, value: int) -> None:

        if value in self.values:
            return
        self.values.add(value)

        if not self.intervals:
            self.intervals.append([value, value])
            return

        idx = bisect_left(self.intervals, [value, value])
        newInterval = [value, value]
        start=end=idx

        if idx > 0 and self.intervals[idx-1][1]+1 == value:
            # merge left
            newInterval[0] = self.intervals[idx-1][0]
            start = idx-1
        if idx < len(self.intervals) and self.intervals[idx][0]-1 == value:
            # merge right
            newInterval[1] = self.intervals[idx][1]
            end = idx+1

        self.intervals[start:end] = [newInterval]

    def getIntervals(self) -> List[List[int]]:

        return self.intervals

"""
Runtime: 159 ms, faster than 86.58% of Python3 online submissions for Data Stream as Disjoint Intervals.
Memory Usage: 19 MB, less than 75.17% of Python3 online submissions for Data Stream as Disjoint Intervals.

"""

if __name__ == '__main__':
    calls = ["SummaryRanges", "addNum", "getIntervals", "addNum", "getIntervals",
             "addNum", "getIntervals", "addNum", "getIntervals", "addNum", "getIntervals"]
    args = [[], [1], [], [3], [], [7], [], [2], [], [6], []]

    for call, arg in zip(calls, args):
        if call == 'SummaryRanges':
            s = SummaryRanges()
        elif call == 'addNum':
            s.addNum(*arg)
        else:
            print(s.getIntervals(*arg))

