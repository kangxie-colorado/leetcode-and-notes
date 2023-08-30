from collections import deque
import math


class Solution:
    def numSquares(self, n: int) -> int:
        

        q = deque()
        q.append((n, 0))

        while q:
            num, steps = q.popleft()
            if steps >= n:
                continue
            if num == 0:
                return steps
            sqrt = int(math.sqrt(num))
            for s in range(sqrt, 0, -1):
                if s*s == n:
                    return steps+1
                q.append((num-s*s, steps+1))
        
        return steps
                
""""
okay.. memory limit execeeded
let me see dp
"""

class Solution:
    def numSquares(self, n: int) -> int:
        dp = [float('inf')]*(n+1)
        dp[1] = 1
        
        for num in range(2,n+1):
            sqrt = int(math.sqrt(num))
            if sqrt*sqrt == num:
                dp[num] = 1
                continue
            
            for s in range(sqrt, 0, -1):
                dp[num] = min(dp[num], dp[num-s*s]+1)
        
        return dp[n]

"""
okay
I see the bfs is better but I missed processing something
that is the pruning

999 -> 990 (can be reached by 999-9 or 999-1(9 times))
it only needs be processed the first time.. the later times are all with higher step(cost)

so yeah.. if it repeats, skip
"""

class Solution:
    def numSquares(self, n: int) -> int:
        

        q = deque()
        q.append((n, 0))
        visited = set()

        while q:
            num, steps = q.popleft()
            if num in visited:
                continue
            visited.add(num)
            if num == 0:
                return steps
            sqrt = int(math.sqrt(num))
            if sqrt*sqrt == n:
                return steps+1
            for s in range(sqrt, 0, -1):

                q.append((num-s*s, steps+1))
        
        return steps


if __name__ == '__main__':
    s = Solution()
    print(s.numSquares(12))