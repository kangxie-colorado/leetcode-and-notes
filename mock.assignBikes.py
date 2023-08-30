"""
maybe a hard problems/
minimize the total dist

1 <= n <= m <= 10
bitmap??
"""

from functools import cache
from typing import List


class Solution:
    def assignBikes(self, workers: List[List[int]], bikes: List[List[int]]) -> int:
        
        @cache
        def f(wIdx, bikeSelected):
            if wIdx == len(workers):
                return 0
            wx,wy = workers[wIdx]

            res = float('inf')
            for bIdx, (bx,by) in enumerate(bikes):
                if (1<<bIdx) & bikeSelected:
                    continue
                res = min(res, abs(wx-bx)+abs(wy-by)+f(wIdx+1, bikeSelected|(1<<bIdx)))
            
            return res
        
        return f(0,0)
            
if __name__ == '__main__':
    s = Solution()
    print(s.assignBikes(workers = [[0,0],[2,1]], bikes = [[1,2],[3,3]]))
    
