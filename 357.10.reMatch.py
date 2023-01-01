"""
https://leetcode.com/problems/regular-expression-matching/

. and *

it is me to do this myself..
I don't know 

probably will get stuck a lot

now I know, the only complexcity comes from *, which is the moderator of previous char
if there is a *, it basically opens up a decision tree.. appear once/twice/..., or appear zero
    - appear zero the j idx should +=2
    - appear once/twice.. the j idx stays at the same 

also using a i idx for s, then this becomes a DP problem
let me see

"""

class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        
        def f(i,j):
            if i>=len(s) and j>=len(p):
                # this shall be the match case
                return True
            if j>=len(p):
                # pattern is used up but string is not finished 
                return False
            
            # i>=len(s) and j<len(s), this remains undecided yet
            # e.g. a vs a*b*, 
            # when i moves to 1.. s is over
            # j will be at 2.. not over.. but b* can become empty therefore a match
            # this will be taken care by b* and * makes decision of zero-appearance 
            
            # no matter what, the leading char must match
            # match = s[i] == s[j] or s[j] == '.'
            # also i could be out of bounds.. so 
            leadingCharMatch = i < len(s) and (s[i] == p[j] or p[j] == '.')
            if j+1<len(p) and p[j+1]=='*':
                # now * opens up the decision tree 
                # zero appearance or one appearance(but not moving j, which is in itself a recursive thing)
                # zero appearance: of course it cannot match s[i] so i should stay put
                # one(and recusive) appearance: the leading char must match.. so i advance by 1
                # and j stays put
                return (f(i, j+2) or (leadingCharMatch and f(i+1, j)))
            else:
                # if there is no *, then this is a char-to-char match
                # if match then both advance by 1
                # otherwise, it is not a match
                return leadingCharMatch and f(i+1, j+1)
            
            return False
        return f(0,0)


"""
Runtime: 3337 ms, faster than 8.62% of Python3 online submissions for Regular Expression Matching.
Memory Usage: 14.2 MB, less than 24.73% of Python3 online submissions for Regular Expression Matching.

adding cache (@cache from functools)

Runtime: 42 ms, faster than 96.00% of Python3 online submissions for Regular Expression Matching.
Memory Usage: 14.1 MB, less than 24.73% of Python3 online submissions for Regular Expression Matching.
"""