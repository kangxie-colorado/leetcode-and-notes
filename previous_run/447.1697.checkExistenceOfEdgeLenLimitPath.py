"""
https://leetcode.com/problems/checking-existence-of-edge-length-limited-paths/?envType=study-plan&id=graph-ii

didn't understand the question quickly -- read again
okay I see
    1. multiple paths.. then maybe I can just to take the lowest one (it is undirected)
    2. it is the individual path's weight < n (not the path total)

how to think of this problem???
totally blank.. ugh!

played 30 mins and still blank
come up see the hint about reorganizing the queries.. 

hum.. interesting.. I'll read the post 

okay.. the insights are

merge all the edges under the query weight together and see if the two points are connected 
to improve the performance - 
    - using two pointers
    - only merge upto query's weight
        if you merge edges with bigger weight.. then you could get false positive
    - then move the pointer accordinglly
    -- yeah, this way it is kind of effcient..

this is kind of subtle and clear.. but when you figure it out.. 
it makes a alot of senes

"""


from typing import List


class Solution:
    def distanceLimitedPathsExist(self, n: int, edgeList: List[List[int]], queries: List[List[int]]) -> List[bool]:
        edgeList.sort(key=lambda x: x[2])
        
        queryAndIdx = [[q,i] for i,q in enumerate(queries)]
        queryAndIdx.sort(key = lambda x: x[0][2])

        roots = [i for i in range(n)]
        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]
        
        def union(x,y):
            roots[find(x)] = roots[find(y)]
        
        edgeIdx = queryIdx = 0
        res = [False] * len(queryAndIdx)
        while queryIdx < len(queryAndIdx):
            q,idx = queryAndIdx[queryIdx]
            n1,n2,d = q

            while edgeIdx < len(edgeList) and edgeList[edgeIdx][2] < d:
                e1,e2,_=edgeList[edgeIdx]
                union(e1,e2)
                edgeIdx += 1
            
            if find(n1) == find(n2):
                res[idx] = True

            queryIdx+=1

        return res

"""
Runtime: 1911 ms, faster than 94.16% of Python3 online submissions for Checking Existence of Edge Length Limited Paths.
Memory Usage: 60.4 MB, less than 60.58% of Python3 online submissions for Checking Existence of Edge Length Limited Paths.
"""

if __name__ == '__main__':
    s = Solution()
    print(s.distanceLimitedPathsExist(n=3, edgeList=[[0, 1, 2], [
          1, 2, 4], [2, 0, 8], [1, 0, 16]], queries=[[0, 1, 2], [0, 2, 5]]))

    print(s.distanceLimitedPathsExist(n=5, edgeList=[[0, 1, 10], [1, 2, 5], [
          2, 3, 9], [3, 4, 13]], queries=[[0, 4, 14], [1, 4, 13]]))
