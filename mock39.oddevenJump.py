"""
the jump is fixed
we can pre-process

O(n**2) cannot pass
then I can do a ranking order???
"""

from functools import cache
from typing import List


class Solution:
    def oddEvenJumps(self, arr: List[int]) -> int:
        
        incrNumIdx = sorted([(n,i) for i,n in enumerate(arr)])
        decrNumIdx = sorted([(n,i) for i,n in enumerate(arr)], key=lambda x: (-x[0], x[1]))


        rawIdxToIncrIdx = {}
        rawIdxToDecrIdx = {}
        for idx, (_,i) in enumerate(incrNumIdx):
            rawIdxToIncrIdx[i] = idx
        for idx, (_,i) in enumerate(decrNumIdx):
            rawIdxToDecrIdx[i] = idx

        @cache
        def f(idx, odd):
            if idx == len(arr)-1:
                return True
            
            A = None
            if odd:
                A = incrNumIdx
                sortIdx = rawIdxToIncrIdx[idx]
            else:
                A = decrNumIdx
                sortIdx = rawIdxToDecrIdx[idx]
            j = sortIdx + 1


            while j < len(A):
                if A[j][1] > idx:
                    return f(A[j][1], not odd)
                j+=1
            
            return False
        
        res = 0
        for i in range(len(arr)):
            res += f(i,True)
        
        return res
            
if __name__ == '__main__':
    s = Solution()
    print(s.oddEvenJumps(arr = [10,13,12,14,15]))