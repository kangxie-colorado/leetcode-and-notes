"""
the question itself is not that easy to understand, took me a few minutes
so this is a greedy???

if there smallest distance, choose it no matter what it cost others
then on tie, breakeven by worker idx
then breakeven by bike idx
"""

from typing import List


class Solution:
    def assignBikes(self, workers: List[List[int]], bikes: List[List[int]]) -> List[int]:
        
        dists = []
        for wIdx,(wX, wY) in enumerate(workers):
            for bIdx, (bX, bY) in enumerate(bikes):
                dists.append((abs(bX-wX)+abs(bY-wY), wIdx, bIdx))
        
        assignedWorks = {}
        assignedBikes = set()
        dists.sort()

        for _, wIdx, bIdx in dists:
            if wIdx in assignedWorks or bIdx in assignedBikes:
                continue
            if len(assignedWorks) == len(workers):
                break

            assignedWorks[wIdx] = bIdx
            assignedBikes.add(bIdx)
        
        res = [0]*len(workers)
        for idx in range(len(workers)):
            res[idx] = assignedWorks[idx]
        
        return res


        