"""
https://leetcode.com/problems/number-of-islands-ii/?envType=study-plan&id=graph-ii

yeah.. so it is basically the unions number after each filling 

I can work on the indexs
- initialize all the m*n to 0.. 
- turn x=0,y=0 to x*n+y=0 -> +1 -> 1
    x=0,y=1 -> 2
- what are neighbor? x diff is 1, meaning index diff by 1 
                                                    ^ (this could be wrong, e.g. when the line wrap around)
    or y diff is 1.. meaning index diff by n
- if I always favor the smaller.. can I get the union number natually? 
    maybe still not.. say 3->2 1
        then 2->1, it will end up 3->1->1, i.e. the 3 is still not updated 

turns out this is wrong
- initialize all the m*n to 0.. 
    if I do this, the find will think the root has always been 0

"""


from typing import List


class Solution:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        roots = [i for i in range(m*n)]

        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]
        
        def union(x,y):
            roots[find(x)]= roots[find(y)]
        
        res = []
        proceesed = set()
        for i in range(len(positions)):
            # union with itself: deal with the starter and not change the results for later
            x1, y1 = positions[i]
            idx1 = x1*n+y1
            proceesed.add(idx1)
            for j in range(i+1):
                x2, y2 = positions[j]
                idx2 = x2*n+y2
                proceesed.add(idx2)
                if idx1 == idx2 or (abs(y1-y2) == 1 and x1==x2) or (abs(x1-x2) == 1 and y1==y2):
                    union(idx1, idx2)
                    
            res.append(len(set(find(r) for r in roots if r in proceesed)))
        
        return res


"""
okay.. passed 92 for first time.. really not bad for me failed
3
3
[[0,1],[1,2],[2,1],[1,0],[0,2],[0,0],[1,1]]
Output:   [1,2,3,4,2,2,1]
Expected: [1,2,3,4,3,2,1]

okay.. because the idx diff by 1 assumption is wrong 
change to 
                if idx1 == idx2 or (abs(y1-y2) == 1 and x1==x2) or (abs(x1-x2) == 1 and y1==y2):
                    union(idx1, idx2)
TLE after 
107 / 162 test cases passed.

okay I see first optimization
when you union with one, you are done with union.. cause you have unioned everybody
adding the break
ah no.. you cannot.. it could union other groups..

if I can avoid the time spent to count union number..?
"""


class Solution:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        roots = [i for i in range(m*n)]

        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]

        def union(x, y):
            roots[find(x)] = roots[find(y)]

        res = []
        processed = set()
        for i in range(len(positions)):
            # union with itself: deal with the starter and not change the results for later
            x1, y1 = positions[i]
            idx1 = x1*n+y1
            if idx1 in processed:
                res.append(res[-1])
                continue

            processed.add(idx1)
            union(idx1, idx1)
            unioned = False
            for j in range(i+1):
                x2, y2 = positions[j]
                idx2 = x2*n+y2
                
                processed.add(idx2)
                if (abs(y1-y2) == 1 and x1 == x2) or (abs(x1-x2) == 1 and y1 == y2):
                    union(idx2, idx1)
                    unioned = True

            if unioned:
                res.append(len(set(find(r) for r in roots if r in processed)))
            else:
                res.append(res[-1]+1 if res else 1)

        return res


"""
cool.. moved a bit further 
and wrong answer

3
3
[[0,0],[0,1],[1,2],[1,2]]

okay.. self vs self...

okay.. still cannot pass the bigger case

ah... why do I need to look thru all the past positions
I only need to look up 4!!
"""


class Solution:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        roots = [i for i in range(m*n)]

        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]

        def union(x, y):
            roots[find(x)] = roots[find(y)]

        res = []
        processed = set()
        for i in range(len(positions)):
            x1, y1 = positions[i]
            idx1 = x1*n+y1
            if idx1 in processed:
                res.append(res[-1])
                continue

            neighborGrps = set()
            for dx,dy in ([-1,0],[1,0],[0,-1],[0,1]):
                x2,y2 = x1+dx,y1+dy
                idx2 = x2*n+y2

                if 0<=x2<m and 0<=y2<n:                        
                    if idx2 in processed:
                        neighborGrps.add(find(idx2))
                        # because I didn't maintain the m*n matrix so I use a map
                        union(idx1, idx2)

            processed.add(idx1)
            # if unioned:
            #     res.append(res[-1] - (len(neighborGrps)-1))
            # else:
            #     res.append(res[-1]+1 if res else 1)
            # equivlent to 
            res.append(res[-1] - (len(neighborGrps)-1) if res else 1)

        return res


"""
okay.. again that line wrap bites me again.. 
I kind of cause confusions for myself

okay.. I should not need to scan everything for the groups number I also only need to scan 4 directions

finally

Runtime: 499 ms, faster than 82.24% of Python3 online submissions for Number of Islands II.
Memory Usage: 19.8 MB, less than 43.36% of Python3 online submissions for Number of Islands II.

okay.. so many subtlities 

the key is only to look up/down/left/right.. and can build current result on top of previous result
"""


class Solution:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        roots = [i for i in range(m*n)]

        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]

        def union(x, y):
            roots[find(x)] = roots[find(y)]

        res = []
        islands = set()
        for i in range(len(positions)):
            x1, y1 = positions[i]
            pos1 = x1*n+y1
            if pos1 in islands:
                res.append(res[-1])
                continue

            neighborGrps = set()
            for dx, dy in ([-1, 0], [1, 0], [0, -1], [0, 1]):
                x2, y2 = x1+dx, y1+dy
                pos2 = x2*n+y2

                if 0 <= x2 < m and 0 <= y2 < n:
                    if pos2 in islands:
                        neighborGrps.add(find(pos2))
                        # because I didn't maintain the m*n matrix so I use a map
                        union(pos1, pos2)

            islands.add(pos1)
            res.append(res[-1] - (len(neighborGrps)-1) if res else 1)

        return res



if __name__ == '__main__':
    s = Solution()
    print(s.numIslands2(m = 3, n = 3, positions = [[0,0],[0,1],[1,2],[2,1]]))
    print(s.numIslands2(m = 3, n = 3, positions = [[0,1],[1,2],[2,1],[1,0],[0,2],[0,0],[1,1]]))
    
