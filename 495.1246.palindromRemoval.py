"""
https://leetcode.com/problems/palindrome-removal/?envType=study-plan&id=dynamic-programming-iii

so it feels like to find the longest palindrom?
so it would like 

f(i,j): represents the min operations to remove all number between i and j, inclusive
if A[i] == A[j], of course they can go together 
    and that means, they can be taken by internal removal
    f(i,j) = f(i+1,j-1)
    e..g removing anything inside i,j can take i,j with them.. not change results
else:
    min(f(i+1,j), f(i,j-1))+1

base:
    i==j: return 1
    i>j: return 0
    i==j-1 and A[i]==A[j]:
        hmm? do I need to specialize this?
        so maybe i<j, I should return 1 as well to generalize this

so yeah.. the solution is clear
give a try
"""


from functools import cache
from typing import List


class Solution:
    def minimumMoves(self, arr: List[int]) -> int:
        @cache
        def f(i,j):
            # print(i,j)
            if i>=j:
                return 1
            
            res = min(f(i+1,j), f(i,j-1))+1
            if arr[i] == arr[j]:
                res = min(res, f(i+1,j-1))
            
            return res

        return f(0,len(arr)-1)

"""
not right yet
[1,4,1,1,2,3,2,1]

this should be done as 1,4,1 followed by 1,2,3,2,1

so it feels like the interval dp pattern?
f(i,j) = min(
    f(i,k) + f(k+1,j) for k in [i+1,j-1]
    if A[i]==A[j]
        it could be f(i+1,j-1)   
)

base are the same?


"""


class Solution:
    def minimumMoves(self, arr: List[int]) -> int:
        @cache
        def f(i, j):
            # print(i,j)
            if i >= j:
                return 1

            res = float('inf')
            if arr[i] == arr[j]:
                res = min(res, f(i+1, j-1))
            for k in range(i,j):
                res = min(res, f(i,k)+f(k+1,j))

            return res

        return f(0, len(arr)-1)
    
"""
Runtime: 6069 ms, faster than 10.14% of Python3 online submissions for Palindrome Removal.
Memory Usage: 33.1 MB, less than 8.70% of Python3 online submissions for Palindrome Removal.

"""




if __name__ == '__main__':
    s = Solution()
    print(s.minimumMoves([1,2]))
    print(s.minimumMoves([1, 3,4,1,5]))
    print(s.minimumMoves([1, 4, 1, 1, 2, 3, 2, 1]))
