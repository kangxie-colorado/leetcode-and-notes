"""
feels like case A onto B.. 
two pointers?
"""

from typing import List


class Solution:
    def intervalIntersection(self, firstList: List[List[int]], secondList: List[List[int]]) -> List[List[int]]:
        def overlap(p1,p2):
            return not (p1[1] < p2[0] or p1[0] > p2[1])

        res = []
        i=j=0
        m,n = len(firstList), len(secondList)
        while i<m and j<n:
            # if firstList[i] overlap with secondList[j]
            # or not
            p1,p2 = firstList[i],secondList[j]
            if overlap(p1,p2):
                res.append([max(p1[0], p2[0]), min(p1[1], p2[1])])

            if p1[1] < p2[1]:
                i+=1
            else:
                j+=1

        return res