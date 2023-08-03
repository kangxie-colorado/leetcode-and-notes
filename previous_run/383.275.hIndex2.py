"""
https://leetcode.com/problems/h-index-ii/submissions/

very confusing 
the thing is l,r represents the possible h 

and h is also the length of that eligible sub-array, there we binary search on l-h(m)-r
and use len(c) - m to get the testing idx.. if it satisfy C[idx] >= m, then keeping this but 
potentially we can go to higher h.. which means moving l to m: l=m, and that means pushing idx further left



"""

from typing import List


class Solution:
    def hIndex(self, C: List[int]) -> int:
        # if C[idx] is a candidate: C[idx] >= len(c)-m+1
        # m is the l-mid-r and in this sense the h papers
        # therefore the idx should len(C)-m-1, e.g. [0,1,3,5,6]
        # when m is 2, the idx should be 3, element-5..
        # h of their n papers have at least h citations each -> C[idx] >= m
        # meaning we have 2 papers having at least 5 citattions
        # we could try more papers: l=m
        # otherwise, the other half.. hard to reason but has to be that way

        # this is after-priori-thoughts.. not in the chrological order in any way
        # what is the l,r?? h is the paper count, so at most the len
        # what is the h representing? idx? or the length of m->edge???
        # it should represnt the length and the idx in C[m] should not be m but be some other calculation
        l, r = 0, len(C)
        while l < r:
            m = r - (r-l)//2  # m as the h
            idx = len(C) - m
            if C[idx] >= m:
                l = m
            else:
                r = m-1

        return l


"""
Runtime: 140 ms, faster than 95.75% of Python3 online submissions for H-Index II.
Memory Usage: 20.6 MB, less than 85.94% of Python3 online submissions for H-Index II.
"""