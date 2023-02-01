"""
https://leetcode.com/problems/number-of-distinct-islands/?envType=study-plan&id=graph-ii

union find
but the twist is distint.. 

interesting
"""


from collections import defaultdict
from typing import List


class Solution:
    def numDistinctIslands(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        roots = {}

        def find(x, y):
            roots.setdefault((x, y), (x, y))

            if roots[x, y] != (x, y):
                roots[x, y] = find(*roots[x, y])

            return roots[x, y]

        def union(x1, y1, x2, y2):
            r1 = find(x1, y1)
            r2 = find(x2, y2)
            if r1<r2:
                roots[r2] = roots[r1]
            else:
                roots[r1] = roots[r2]

        for i in range(m):
            for j in range(n):

                # only union my left/up.. that would be fine
                if grid[i][j]:
                    # at least union with itself otherwise, roots cannot be populated
                    union(i, j, i, j)
                    if i > 0 and grid[i-1][j]:
                        union(i, j, i-1, j)
                    if j > 0 and grid[i][j-1]:
                        union(i, j, i, j-1)

        grpSet = defaultdict(list)
        for i in range(m):
            for j in range(n):
                if grid[i][j]:
                    r = find(i, j)
                    grpSet[r].append((i-r[0],j-r[1]))

        
        # how to tell distinct?
        # notice the append is by row/col.. so the (i,j) pairs are natuarally sorted
        # we can minus the first element or minus the root.. 
        # not safe.. then I can union to smaller root
        groupSets = list(grpSet.values())
        duplicate = set()
        
        for i in range(len(groupSets)):
            for j in range(i+1, len(groupSets)):
                grp1, grp2 = groupSets[i], groupSets[j]
                if grp1 == grp2:
                    duplicate.add(j)
        return len(groupSets) - len(duplicate)

"""
Runtime: 501 ms, faster than 27.19% of Python3 online submissions for Number of Distinct Islands.
Memory Usage: 15.8 MB, less than 80.02% of Python3 online submissions for Number of Distinct Islands.
"""

if __name__ == '__main__':
    s = Solution()
    print(s.numDistinctIslands([[0,1,0],[1,0,1]]))