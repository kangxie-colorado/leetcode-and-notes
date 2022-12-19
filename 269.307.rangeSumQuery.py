"""
https://leetcode.com/problems/range-sum-query-mutable/


I don't how to make the most efficient data structure
but I think
use a partial sum to deliver the range sum quickly.. that is of course the way
but the trouble is with the update.. it change all the partital sums coming after this item

so how to balance these two operatios...
a bit difficult...


"""


from typing import List
from sortedcontainers import SortedList


class NumArray:

    def __init__(self, nums: List[int]):
        self.nums = nums
        self.deltaList = SortedList()
        self.rangeSums = [0] + nums
        prefix = 0
        for i, rs in enumerate(self.rangeSums):
            self.rangeSums[i] += prefix
            prefix += rs

    def update(self, index: int, val: int) -> None:
        insertAt = self.deltaList.bisect_left((index, -100))
        if insertAt < len(self.deltaList) and self.deltaList[insertAt][0] == index:
            del self.deltaList[insertAt]

        if val-self.nums[index] != 0:
            self.deltaList.add((index, val-self.nums[index]))

    def sumRange(self, left: int, right: int) -> int:
        if right+1 >= len(self.rangeSums):
            return 0

        deltaLeft = self.deltaList.bisect_left((left-0.1, 0))
        deltaRight = self.deltaList.bisect_right((right+0.1, 0))
        deltaSum = sum([i[1] for i in self.deltaList[deltaLeft:deltaRight]])

        return self.rangeSums[right+1] - self.rangeSums[left] + deltaSum


"""
pass 9/16 and TLE
so sign.. I don't know an efficient way

just looking at the solutions
binary-indexed tree and segment tree

okay... I never heard about it...

update 12/12: now I heard about it and did probelm 315 with it
think I can crack it better now
"""


class NumArray:

    def __init__(self, nums: List[int]):
        self.nums = [0]*len(nums)
        self.bi_tree = [0] * (len(nums)+1)
        for i, n in enumerate(nums):
            self.update(i, n)

    def update(self, index: int, val: int) -> None:
        delta = val-self.nums[index]
        i = 1 + index
        while i <= len(self.nums):
            self.bi_tree[i] += delta
            lsb = i & -i
            i += lsb
        self.nums[index] = val

    def get(self, index: int) -> int:
        S = 0
        while index > 0:
            S += self.bi_tree[index]
            lsb = index & -index
            index -= lsb

        return S

    def sumRange(self, left: int, right: int) -> int:

        # sum(right+1) - sum(left); bi_tree is 1-based
        return self.get(right+1) - self.get(left)


"""
Runtime: 5143 ms, faster than 46.23% of Python3 online submissions for Range Sum Query - Mutable.
Memory Usage: 31.3 MB, less than 73.60% of Python3 online submissions for Range Sum Query - Mutable.

Runtime: 1907 ms, faster than 95.84% of Python3 online submissions for Range Sum Query - Mutable.
Memory Usage: 31.2 MB, less than 80.27% of Python3 online submissions for Range Sum Query - Mutable.

>>> the trick is to init self.nums to [0]*n
>>> then update the vals into it... 

don't do it in two ways.. it will backfire

and then segment tree solution is next
"""


class SegmentTreeNode:
    def __init__(self, start, end, rangeSum=0, left=None, right=None) -> None:
        self.start = start
        self.end = end
        self.rangeSum = rangeSum
        self.left = left
        self.right = right


class NumArray:

    def __init__(self, nums: List[int]):
        self.root = self.build_segment_tree(nums)
        self.nums = nums

    def build_segment_tree(self, nums):
        def f(start, end):
            if start == end:
                return SegmentTreeNode(start, end, nums[start])

            mid = start + (end - start)//2
            # [start to mid] inclusive numbers used in left side, not use mid as root
            # some conceptual hiding here
            left = f(start, mid)
            right = f(mid+1, end)
            return SegmentTreeNode(start, end, left.rangeSum+right.rangeSum, left, right)

        return f(0, len(nums)-1)

    def update(self, index: int, val: int) -> None:
        delta = val - self.nums[index]

        def f(node: SegmentTreeNode):
            if node.start == node.end == index:
                node.rangeSum += delta
                return

            mid = node.start + (node.end-node.start)//2
            if mid < index:
                f(node.right)
            else:
                f(node.left)
            node.rangeSum = node.left.rangeSum + node.right.rangeSum
        f(self.root)
        self.nums[index] = val

    def sumRange(self, left: int, right: int) -> int:
        def f(node, l, r):
            # no need to test against None
            # the base case is only at leafs
            if node.start == l and node.end == r:
                return node.rangeSum

            mid = node.start + (node.end - node.start)//2
            if mid < l:
                return f(node.right, l, r)
            elif mid >= r:
                return f(node.left, l, r)
            else:
                return f(node.left, l, mid) + f(node.right, mid+1, r)

        return f(self.root, left, right)


"""
Runtime: 8309 ms, faster than 11.91% of Python3 online submissions for Range Sum Query - Mutable.
Memory Usage: 49.6 MB, less than 13.54% of Python3 online submissions for Range Sum Query - Mutable.

basically I watched a video and had the idea what segment tree is about
now I build it up and applied it to some leetcode problem

and it worked
so I think this is at least a good thing to do and gave me a little pat on the back .. I can code up with ideas. 
"""


if __name__ == '__main__':
    s = NumArray([1, 2, 3, 4, 5])

    print(s.sumRange(0, 2))
    print(s.sumRange(0, 3))
    print(s.sumRange(3, 4))

    s.update(3, 2)
    print(s.sumRange(0, 2))
    print(s.sumRange(0, 3))
    print(s.sumRange(3, 4))

    s.update(3, 4)
    print(s.sumRange(0, 2))
    print(s.sumRange(0, 3))
    print(s.sumRange(3, 4))

    s.update(3, 5)
    s.update(4, 6)
    print(s.sumRange(0, 2))
    print(s.sumRange(0, 3))
    print(s.sumRange(3, 4))

    s.update(3, 5)
    s.update(4, 6)
    print(s.sumRange(0, 2))
    print(s.sumRange(0, 3))
    print(s.sumRange(3, 4))
