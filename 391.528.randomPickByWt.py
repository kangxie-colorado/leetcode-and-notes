"""
https://leetcode.com/problems/random-pick-with-weight/?envType=study-plan&id=binary-search-ii


interesting 
so if I can lay all numbers flat.. that is trivial but the memory is a problem 

so let me see 
[1,3] - means a random number between 1 and 4
a, b,b,b
or prefixSum 0 1 4
if it is 1, then 1
2-4, it it is 4.. 

looks like it.. 

"""


import bisect
import random
from typing import List


class Solution:

    def __init__(self, w: List[int]):
        self.summ = [0]*(len(w)+1)

        for i in range(1, len(w)+1):
            self.summ[i] = self.summ[i-1] + w[i-1]


    def pickIndex(self) -> int:
        num = random.randint(1, self.summ[-1])
        idx = bisect.bisect_left(self.summ, num)
        return idx-1

if __name__ == '__main__':
    calls = ["Solution","pickIndex"]
    args = [[[1]],[]]

    for call,arg in zip(calls, args):
        if call == "Solution":
            s = Solution(*arg)
        else:
            print(s.pickIndex(*arg))

"""
Runtime: 214 ms, faster than 89.54% of Python3 online submissions for Random Pick with Weight.
Memory Usage: 18.5 MB, less than 60.21% of Python3 online submissions for Random Pick with Weight.
"""