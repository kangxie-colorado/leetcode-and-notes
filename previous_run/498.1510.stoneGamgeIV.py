"""
https://leetcode.com/problems/stone-game-iv/

should not be very difficult
"""


from functools import cache
import math


class Solution:
    def winnerSquareGame(self, n: int) -> bool:

        @cache
        def f(i):
            if i == 0:
                return False

            s = int(math.sqrt(i))
            for j in range(s,0,-1):
                if not f(i-j*j):
                    return True
            
            return False
        
        return f(n)

"""
Runtime: 169 ms, faster than 99.39% of Python3 online submissions for Stone Game IV.
Memory Usage: 18.7 MB, less than 33.43% of Python3 online submissions for Stone Game IV.

"""

if __name__ == '__main__':
    s = Solution()
    print(s.winnerSquareGame(1))
    print(s.winnerSquareGame(2))
    print(s.winnerSquareGame(4))

            

