"""
did this before but forgot

so okay, three scenarios 
1. to the left  <= A[0]-1
2. in the middle 
    A[-1] - A[0] - len(A) + 1 <- this many number is missing in the array
3. to the right
  
"""
import bisect
from typing import List


class Solution:
    def findKthPositive(self, arr: List[int], k: int) -> int:
        leftMissing = arr[0] - 1
        inArrayMissing = arr[-1] - arr[0] -len(arr)+1

        if k<=leftMissing:
            return k
        if k>leftMissing+inArrayMissing:
            return arr[-1] + k - (leftMissing+inArrayMissing)
        
        # now solve the in-array missing
        l,r = arr[0], arr[-1]
        while l<r:
            m = l + (r-l)//2
            idx = bisect.bisect_left(arr, m)

            if arr[idx] == m:
                # m is in arr
                # missing m-idx-1 in front of this one
                # notice the -1, different than when m is not in array
                if (m-idx-1) < k:
                    l = m+1
                else:
                    r = m-1
            else:
                # m is not in arr
                # in front of m, there are idx numbers 
                # so I am (m - idx)-th missing number
                if (m-idx) == k:
                    return m
                if (m-idx) < k:
                    l = m+1
                else:
                    r = m-1
        
        return l

if __name__ == '__main__':
    s = Solution()
    print(s.findKthPositive(arr = [2,7,10,13,16,23,29,32,35,50], k = 2))