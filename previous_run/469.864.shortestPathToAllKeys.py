"""
https://leetcode.com/problems/shortest-path-to-get-all-keys/?envType=study-plan&id=graph-ii

bfs
states to avoid cycle, x,y,keys

on the tip of bfs -- 
    encoutering a key.. update the key.. continue to 4 directions or append queue and let next loop
    enoutering a lock.. if the key is in hans.. continue to 4 directions as usual.. otherwise.. skip

    could be doing this at either end of bfs?
    I will see

thoughts on maintaining keys
    thought of using sorted string because only 6 keys
    then something better comes up using a bitmap


"""


from collections import defaultdict, deque
from typing import List


class Solution:
    def shortestPathAllKeys(self, grid: List[str]) -> int:
        dirs = [[1,0], [-1,0], [0,1], [0,-1]]

        m,n = len(grid), len(grid[0])
        q = deque()
        keysBitMap = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '@':
                    q.append((i,j,0,0))   # x,y,keys,cost
                if grid[i][j] in 'abcdef':
                    keysBitMap |= 1 << (ord(grid[i][j])-ord('a'))
        
        visited = defaultdict(int)
        while q:
            x,y,keys,cost = q.popleft()
            print("top", x,y,keys,cost)
            if keys == keysBitMap:
                # all keys acquired
                return cost

            if (x,y,keys) in visited and visited[x,y,keys]<=cost:
                continue
            visited[x, y, keys] = cost

            for dx,dy in dirs:
                nx,ny = x+dx,y+dy
                if 0<=nx<m and 0<=ny<n:
                    # print(nx, ny, grid[nx][ny])
                    if grid[nx][ny] in '@.':
                        # just pass by
                        q.append((nx,ny, keys, cost+1))
                    if grid[nx][ny] in 'abcedf':
                        # just update the key and pass by regularly
                        # need to avoid cross iteration inference
                        # say A.a .. if I come down to . from up
                        # then I see a update the key then I see A.. opened it...
                        # and that is wrong...
                        newKeys = keys | 1<<(ord(grid[nx][ny])-ord('a'))
                        q.append((nx,ny, newKeys, cost+1))
                    if grid[nx][ny] in 'ABCDEF':
                        # a lock: if key is in had.. continue as normal
                        # otherwise: cannot add to queue
                        if keys & 1 << (ord(grid[nx][ny])-ord('A')):
                            q.append((nx, ny, keys, cost+1))
                    # print("bottom", nx, ny, grid[nx][ny], keys)

        return -1

"""
Runtime: 396 ms, faster than 68.90% of Python3 online submissions for Shortest Path to Get All Keys.
Memory Usage: 18.3 MB, less than 91.42% of Python3 online submissions for Shortest Path to Get All Keys.

must take break when stuck!!!!
"""


class Solution:
    def shortestPathAllKeys(self, grid: List[str]) -> int:
        dirs = [[1, 0], [-1, 0], [0, 1], [0, -1]]

        m, n = len(grid), len(grid[0])
        q = deque()
        keysBitMap = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == '@':
                    q.append((i, j, 0, 0))   # x,y,keys,cost
                if grid[i][j] in 'abcdef':
                    keysBitMap |= 1 << (ord(grid[i][j])-ord('a'))

        visited = defaultdict(int)
        while q:
            x, y, keys, cost = q.popleft()
            # print(x,y,keys,cost)
            if keys == keysBitMap:
                # all keys acquired
                return cost

            if (x, y, keys) in visited and visited[x, y, keys] <= cost:
                continue
            visited[x, y, keys] = cost

            for dx, dy in dirs:
                nx, ny = x+dx, y+dy
                if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] != '#':
                    if grid[nx][ny] in '@.' or (grid[nx][ny] in 'ABCDEF' and keys & 1 << (ord(grid[nx][ny])-ord('A'))):
                        # just pass by if it is empty
                        # or a lock: if key is in had.. continue as normal
                        #   otherwise: cannot add to queue
                        q.append((nx, ny, keys, cost+1))

                    if grid[nx][ny] in 'abcedf':
                        # just update the key and pass by regularly
                        q.append((nx, ny, keys | 1 << (
                            ord(grid[nx][ny])-ord('a')), cost+1))

        return -1

"""
Runtime: 380 ms, faster than 71.31% of Python3 online submissions for Shortest Path to Get All Keys.
Memory Usage: 18.4 MB, less than 87.94% of Python3 online submissions for Shortest Path to Get All Keys.
"""

if __name__ == '__main__':
    s = Solution()
    print(s.shortestPathAllKeys(grid=["@...a", ".###A", "b.BCc"]))
    # print(s.shortestPathAllKeys(grid = ["@.a..","###.#","b.A.B"]))
    # print(s.shortestPathAllKeys(grid = ["@..aA","..B#.","....b"]))
    # print(s.shortestPathAllKeys(grid=["@Aa"]))

