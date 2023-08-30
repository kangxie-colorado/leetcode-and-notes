import bisect
from collections import defaultdict
from typing import List


class Solution:
    def shortestDistanceColor(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        colorList = defaultdict(list)
        for idx,color in enumerate(colors):
            colorList[color].append(idx)
        
        res = []
        for idx,color in queries:
            if color not in colorList:
                res.append(-1)
                continue

            searchIdx = bisect.bisect_left(colorList[color], idx)
            
            if searchIdx == 0:
                closest = colorList[color][0]
            elif searchIdx == len(colorList[color]):
                closest = colorList[color][-1]
            elif colorList[color][searchIdx] == idx:
                closest = idx
            else:
                closest = colorList[color][searchIdx] 
                if abs(colorList[color][searchIdx-1] - idx) < abs(closest - idx):
                    closest = colorList[color][searchIdx-1]
            res.append(abs(closest-idx))
        return res


if __name__ == '__main__':
    s = Solution()
    print(s.shortestDistanceColor([2,1,2,2,1], [[1,1],[4,3],[1,3],[4,2],[2,1]]))