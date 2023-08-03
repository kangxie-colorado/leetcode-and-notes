"""https://leetcode.com/problems/zigzag-iterator/?envType=study-plan&id=programming-skills-iii

okay.. maybe this is not a super difficult problem
I see a solutino just to switch between two arrays

and when some arrary is emtpy, switch to right.. 

"""

from typing import List


class ZigzagIterator:
    def __init__(self, v1: List[int], v2: List[int]):
        self.vectors = [v1, v2]
        self.indexs = [0,0]
        self.array = 0

    def next(self) -> int:
        choice = self.array
        if self.indexs[choice] >= len(self.vectors[choice]):
            choice ^= 1
        
        res = self.vectors[choice][self.indexs[choice]]
        self.indexs[choice] += 1
        self.array ^= 1

        return res

    def hasNext(self) -> bool:
        return sum(i for i in self.indexs) < sum(len(a) for a in self.vectors)


"""
Runtime: 64 ms, faster than 70.91% of Python3 online submissions for Zigzag Iterator.
Memory Usage: 14.4 MB, less than 39.70% of Python3 online submissions for Zigzag Iterator.
"""