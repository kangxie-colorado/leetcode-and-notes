"""
https://leetcode.com/problems/different-ways-to-add-parentheses/

solution is not obvious

"""


from ast import operator
from itertools import count
from typing import List


class Solution:
    def diffWaysToCompute(self, expression: str) -> List[int]:

        def helper(exp):
            m = []
            for i, c in enumerate(exp):
                if c in '+-*':
                    m.append(i)
            if len(m) == 0:
                return [int(exp)]
            res = []
            for i in m:
                left = helper(exp[:i])
                right = helper(exp[i+1:])
                for n1 in left:
                    for n2 in right:
                        op = exp[i]
                        if op == '+':
                            res.append(n1+n2)
                        if op == '-':
                            res.append(n1-n2)
                        if op == '*':
                            res.append(n1*n2)
            return res
        return helper(expression)


"""
Runtime: 45 ms, faster than 76.26% of Python3 online submissions for Different Ways to Add Parentheses.
Memory Usage: 14.1 MB, less than 17.36% of Python3 online submissions for Different Ways to Add Parentheses.

wowo... not bad...

Runtime: 62 ms, faster than 40.01% of Python3 online submissions for Different Ways to Add Parentheses.
Memory Usage: 13.9 MB, less than 84.66% of Python3 online submissions for Different Ways to Add Parentheses.

okay... previously I came up the idea as above..
it is kind of like brute force

basically treat each operator as a divide, and split that into two parts.. 
then we can solve left and solve right and multiple the results

notice the searching for operators is repeated in each run.. can I do better?
also instead of using the partial string.. can I just pass in the l,r and thus use cache and dynamic programming?
"""


class Solution:
    def diffWaysToCompute(self, exp: str) -> List[int]:
        m = []
        for i, c in enumerate(exp):
            if c in '+-*':
                m.append(i)
        
        cache = {}

        def helper(l,r):
            if (l,r) in cache:
                return cache[l,r]
            res = []
            for i in m:
                if l<i<r:
                    left = helper(l, i)
                    right = helper(i+1, r)
                    for n1 in left:
                        for n2 in right:
                            op = exp[i]
                            if op == '+':
                                res.append(n1+n2)
                            if op == '-':
                                res.append(n1-n2)
                            if op == '*':
                                res.append(n1*n2)
            # notice there is no base case on the top
            # because to test exp[l:r].isdigit() would be that base case
            # but that would require O(r-l) time for each..
            # so actually the base case if default at the bottom
            # when there is no split.. it must be digit itself... 
            # this is kind of a hidden property 
            # aslo kind of this is like post-order traversal?
            if not res:
                res = [int(exp[l:r])]
            cache[l, r] = res
            return res
        
        return helper(0, len(exp))

"""
Runtime: 58 ms, faster than 66.58% of Python3 online submissions for Different Ways to Add Parentheses.
Memory Usage: 14 MB, less than 50.72% of Python3 online submissions for Different Ways to Add Parentheses.

let me add cache

Runtime: 42 ms, faster than 84.01% of Python3 online submissions for Different Ways to Add Parentheses.
Memory Usage: 14.2 MB, less than 18.93% of Python3 online submissions for Different Ways to Add Parentheses.

yeah.. cache makes it run faster.. 
Runtime: 33 ms, faster than 95.63% of Python3 online submissions for Different Ways to Add Parentheses.
Memory Usage: 14 MB, less than 82.78% of Python3 online submissions for Different Ways to Add Parentheses.

now this looks like a dp problem also
"""



if __name__ == '__main__':
    s = Solution()
    print(s.diffWaysToCompute('2-1-1'))
    print(s.diffWaysToCompute('2*3-4*5'))
