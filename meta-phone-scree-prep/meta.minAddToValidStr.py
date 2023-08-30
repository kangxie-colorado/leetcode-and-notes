"""
not sure which problem this
but to get the minimal add to make str valid

it is actually same as minimal remove
and I did that in a previous problem..

and can be used without change
"""

"""
https://leetcode.com/problems/minimum-add-to-make-parentheses-valid/
problem 921 

"""

class Solution:
    def minAddToMakeValid(self, s: str) -> int:
        def miniRemoval(s):
            stack = []
            left=right=0
            for c in s:
                if c not in '()':
                    continue
                
                if c=='(':
                    stack.append(c)
                else:
                    if not stack or stack[-1] != '(':
                        right += 1
                    else:
                        stack.pop()

            left += len(stack)
            return left,right
        l,r = miniRemoval(s)
        return l+r