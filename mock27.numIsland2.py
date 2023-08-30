from typing import List


class Solution:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        roots = {}
        def find(x):
            if x!=roots[x]:
                roots[x] = find(roots[x])
            return roots[x]

        def union(x,y):
            if x>y:
                x,y=y,x
            roots[find(x)] = find(roots[y])

        res = []
        flatPos = []
        for x,y in positions:
            pos = x*n+y
            roots[pos] = pos
            if not res:
                res.append(1)
                flatPos.append(pos)
                continue
            
            for lastPos in flatPos:
                lastX,lastY = lastPos//n,lastPos%n
                if abs(x-lastX)+abs(y-lastY)==1:
                      union(lastPos, pos)
            
            grps = set()
            for k in roots:
                grps.add(find(k))
            
            res.append(len(grps))
            flatPos.append(pos)
        
        return res

"""
okay, at least now this passes correctness
it will TLE 

now lets think about the optimization
yeah, the first is only to look 4-dirs, not all the previous

"""

class Solution:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        roots = {}
        def find(x):
            roots.setdefault(x,x)
            if x!=roots[x]:
                roots[x] = find(roots[x])
            return roots[x]

        def union(x,y):
            if x>y:
                x,y=y,x
            roots[find(x)]= roots[find(y)]

        res = []
        flatPos = set()
        for x,y in positions:
            pos = x*n+y
            union(pos,pos)
            if not res:
                res.append(1)
                flatPos.add(pos)
                continue
            
            for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx,ny = x+dx,y+dy
                nPos = nx*n+ny
                if 0<=nx<m and 0<=ny<n and nPos in flatPos:
                    union(pos, nPos)
            
            grps = set()
            for k in roots:
                grps.add(find(k))
            
            res.append(len(grps))
            flatPos.add(pos)
        
        return res

"""
still TLE
so the optimization is how many groups it connected
"""
class Solution:
    def numIslands2(self, m: int, n: int, positions: List[List[int]]) -> List[int]:
        roots = [i for i in range(m*n)]
        def find(x):
            if x!=roots[x]:
                roots[x] = find(roots[x])
            return roots[x]
        def union(x,y):
            roots[find(x)] = roots[find(y)]
        
        res = []
        flatPos = set()
        for x,y in positions:
            pos = x*n+y
            if not res:
                res.append(1)
                flatPos.add(pos)
                continue
            if pos in flatPos:
                res.append(res[-1])
                continue
            connectedGrp = set()
            for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx,ny = x+dx,y+dy
                nPos = nx*n+ny
                if 0<=nx<m and 0<=ny<n and nPos in flatPos:
                    connectedGrp.add(find(nPos))
                    union(pos, nPos)
            
            if not connectedGrp:
              res.append(res[-1]+1)
            else:
              res.append(res[-1]-(len(connectedGrp)-1))
            flatPos.add(pos)
        
        return res

if __name__ == '__main__':
    s = Solution()
    # print(s.numIslands2(2,2,[[0,0],[1,1],[0,1]]))
    print(s.numIslands2(3,3,[[0,1],[1,2],[2,1],[1,0],[0,2],[0,0],[1,1]]))
            

        