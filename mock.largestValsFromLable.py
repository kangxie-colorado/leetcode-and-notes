from collections import defaultdict
import heapq
from typing import List


class Solution:
    def largestValsFromLabels(self, values: List[int], labels: List[int], numWanted: int, useLimit: int) -> int:
        h  = []
        for value,label in zip(values,labels):
            heapq.heappush(h,(-value, label))
        
        used = defaultdict(int)
        res = 0
        while numWanted:
            value,label = heapq.heappop(h)
            if used[label] >= useLimit:
                continue
            used[label] += 1
            res += abs(value)
        
        return res

            