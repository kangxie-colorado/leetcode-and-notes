"""
not much to think about

but thinking this
1. removing all parenthesis, it will be valid!
2. how about I think it in reverse way
remove all parentheses
add pairs back???

or maybe
1. figure out the minimum removal 
  mini removal of left and right
2. then apply that to get uniq strings


"""

from collections import deque
from typing import List


class Solution:
    def removeInvalidParentheses(self, s: str) -> List[str]:
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
        
        leftRm,rightRm = miniRemoval(s)

        # get all positions of left and right ()
        leftParens = []
        rightParens = []
        for idx,c in enumerate(s):
            if c=='(':
                leftParens.append(idx)
            if c==')':
                rightParens.append(idx)

        # how to apply the remavals???
        def applyRemoval(idx, postions, removal):
            # process idx position 
            # remove or not remove
            if removal == 0:
                return [postions[idx:]]
            if removal == len(postions)-idx:
                return [[]]
            
            res = []
            # not removing this one
            leftCombs = [[postions[idx]]]
            rightCombs = applyRemoval(idx+1, postions, removal)
            
            for lc in leftCombs:
                for rc in rightCombs:
                    res.append(lc+rc)
            
            # removing this one
            rightCombs = applyRemoval(idx+1, postions, removal-1)
            for rc in rightCombs:
                res.append(rc)
            
            return res
        
        # print(leftParens)
        # print(rightParens)

        # print(applyRemoval(0, leftParens, leftRm))
        # print(applyRemoval(0, rightParens, rightRm))

        leftCombs = applyRemoval(0, leftParens, leftRm)
        rightCombs = applyRemoval(0, rightParens, rightRm)

        def isValid(lc, rc):
            i=j=0
            stack = []

            while  j<len(rc):
                if i<len(lc) and lc[i] < rc[j]:
                    stack.append('(')
                    i+=1
                else:
                    # a ')' 
                    if not stack or stack[0]!='(':
                        return False
                    stack.pop()
                    j+=1
            return len(stack)==0

        def getStr(lc, rc):
            res = []
            allPs = set(lc+rc)
            for i,c in enumerate(s):
                if c in '()' and i not in allPs:
                    continue
                
                res.append(c)
            return "".join(res)
            
        res = set()
        for lc in leftCombs:
            for rc in rightCombs:
                if isValid(lc, rc):
                    res.add(getStr(lc,rc))
        return list(res)


"""
this solution worked but very long/complicated
I read and saw there is a simpler one - bfs

I think I got that idea, let me code it up
"""


class Solution:
    def removeInvalidParentheses(self, s: str) -> List[str]:
        def isValid(substr):
            stack = []
            for chr in subStr:
                if chr not in '()':
                    continue
                
                if chr == '(':
                    stack.append(chr)
                else:
                    if not stack:
                        return False
                    stack.pop()
            return len(stack) == 0 
                
        q = deque()
        q.append(s)
        found = False
        res = set()
        visited = set()
        visited.add(s)
      
        while q:
            sz = len(q)
            while sz:
                subStr = q.popleft()
                sz -= 1
                
                if isValid(subStr):
                    found = True
                    res.add(subStr)
                
                if not found:
                    for idx,chr in enumerate(subStr):
                        if chr not in '()':
                            continue
                        t = subStr[:idx]+subStr[idx+1:]
                        if t in visited: 
                            continue
                        
                        q.append(t)
                        visited.add(t)
        
        return list(res)


if __name__ == '__main__':
    s = Solution()
    print(s.removeInvalidParentheses(s = "()())()"))
    # print(s.removeInvalidParentheses(s = "(a)())()"))
    # print(s.removeInvalidParentheses(s = ")("))
                    
                    
                        