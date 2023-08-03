"""
https://leetcode.com/problems/reconstruct-itinerary/
DFS + Backtrack
"""


from collections import defaultdict
from typing import List


class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        tickets.sort()
        graph = defaultdict(list)
        for s, d in tickets:
            graph[s].append(d)

        res = ['JFK']
        def dfs(ap):
            if len(res) == len(tickets)+1:
                return True

            if ap not in graph:
                return False
            # deep copy here
            temp = list(graph[ap])
            for i, nextAP in enumerate(temp):
                graph[ap].pop(i)
                res.append(nextAP)
                if dfs(nextAP):
                    return True
                res.pop()
                # deep copy here too -- must
                graph[ap] = list(temp)

            return False

        dfs('JFK')
        return res
"""
Runtime: 93 ms, faster than 83.13% of Python3 online submissions for Reconstruct Itinerary.
Memory Usage: 14.9 MB, less than 16.30% of Python3 online submissions for Reconstruct Itinerary.
"""

if __name__ == '__main__':
    s = Solution()
    print(s.findItinerary([["JFK","KUL"],["JFK","NRT"],["NRT","JFK"]]))