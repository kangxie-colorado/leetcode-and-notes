"""
https://leetcode.com/problems/the-earliest-moment-when-everyone-become-friends/?envType=study-plan&id=graph-ii

seems like sort then union find..
maybe no need to sort

just record the time when edges == n-1
hmm.. still sort
"""


from typing import List


class Solution:
    def earliestAcq(self, logs: List[List[int]], n: int) -> int:
        logs.sort()

        roots = list(range(n))

        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]

        def union(x, y):
            roots[find(x)] = roots[find(y)]

        edges = 0
        # use union find's property so that
        # the redundant connections are not added
        # meaning all edges are non-redudant and when the total edges reach n-1
        # meaning all friends are connected.. therefore that is the time to return
        for t, f1, f2 in logs:
            if find(f1) != find(f2):
                union(f1, f2)
                edges += 1
                if edges == n-1:
                    return t

        return -1

"""
Runtime: 116 ms, faster than 73.42% of Python3 online submissions for The Earliest Moment When Everyone Become Friends.
Memory Usage: 14.2 MB, less than 96.11% of Python3 online submissions for The Earliest Moment When Everyone Become Friends.

checked lee's code
    def earliestAcq(self, logs, N):
        uf = {x: x for x in xrange(N)}
        self.groups = N

        def merge(x, y):
            x, y = find(x), find(y)
            if x != y:
                self.groups -= 1
                uf[x] = y

        def find(x):
            if uf[x] != x:
                uf[x] = find(uf[x])
            return uf[x]

        for t, x, y in sorted(logs):
            merge(x, y)
            if self.groups == 1:
                return t
        return -1

he overload the union function with more functionality and count down
same idea but always a pleasant sight to see the code
"""