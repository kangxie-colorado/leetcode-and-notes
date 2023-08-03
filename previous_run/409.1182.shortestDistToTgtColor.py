"""
https://leetcode.com/problems/shortest-distance-to-target-color/

just thinking pre-compute the closest distance for 1/2/3 color for each element 
scan from left, scan from right.. take min..

seems easy..
"""


from typing import List


class Solution:
    def shortestDistanceColor(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        leftDists = [None] * len(colors)
        colorDist = [0, float('inf'), float('inf'), float('inf')]
        for i,c in enumerate(colors):
            for cIdx in range(1,4):
                if c == cIdx:
                    colorDist[cIdx] = 0
                else:
                    colorDist[cIdx] += 1
            leftDists[i] = list(colorDist)
        
        rightDists = [None] * len(colors)
        colorDist = [0, float('inf'), float('inf'), float('inf')]
        for i, c in enumerate(colors[::-1]):
            for cIdx in range(1,4):
                if c == cIdx:
                    colorDist[cIdx] = 0
                else:
                    colorDist[cIdx] += 1
            rightDists[len(colors)-i-1] = list(colorDist)


        dists = [None] * len(colors)
        for i in range(len(dists)):
            dists[i] = [
                min(l,r) for l,r in zip(leftDists[i], rightDists[i])
            ]
        
        res = [0]*len(queries)
        for i,(idx,color) in enumerate(queries):
            res[i] = dists[idx][color] if dists[idx][color] is not float('inf') else -1
        return res


"""
Runtime: 2350 ms, faster than 52.78% of Python3 online submissions for Shortest Distance to Target Color.
Memory Usage: 43.6 MB, less than 5.25% of Python3 online submissions for Shortest Distance to Target Color.
"""

if __name__ == '__main__':
    s = Solution()
    print(s.shortestDistanceColor(colors = [1,1,2,1,3,2,2,3,3], queries = [[1,3],[2,2],[6,1]]))