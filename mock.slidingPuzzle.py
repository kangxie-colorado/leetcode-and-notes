"""
treat this like a dfs search

the state variable can be string, "412,503"
from state to figure next move

"""


from collections import deque
from typing import List


class Solution:
    def slidingPuzzle(self, board: List[List[int]]) -> int:
        
        visited = set()
        q = deque()

        def boardToStr(b):
            return "".join([str(b) for b in b[0]]) + "".join([str(b) for b in b[1]])
        
        def posOf0(s):
            idx = s.index('0')
            return idx//3, idx%3
        
        def nextStrs(s):
            x0,y0 = posOf0(s)

            res = []
            for dx,dy in [(-1,0),(1,0), (0,-1), (0,1)]:
                nx,ny = x0+dx, y0+dy
                if 0<=nx<2 and 0<=ny<3:
                    listStr = list(s)
                    swapIdx = nx*3+ny
                    zeroIdx = x0*3+y0
                    listStr[swapIdx], listStr[zeroIdx] = listStr[zeroIdx], listStr[swapIdx]
                    res.append("".join(listStr))
            return res

        initial = boardToStr(board)
        q.append((initial, 0))

        while q:
            stackTopStr,step = q.popleft()
            if stackTopStr == '123450':
                return step
            
            if stackTopStr in visited:
                continue
            visited.add(stackTopStr)

            for nextstr in nextStrs(stackTopStr):
                q.append((nextstr, step+1))
        
        return -1


if __name__ == '__main__':
    s = Solution()
    print(s.slidingPuzzle(board = [[1,2,3],[4,0,5]]))
    print(s.slidingPuzzle(board = [[1,2,3],[5,4,0]]))
    print(s.slidingPuzzle(board = [[4,1,2],[5,0,3]]))