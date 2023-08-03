"""
https://leetcode.com/problems/satisfiability-of-equality-equations/?envType=study-plan&id=graph-ii

interesting.. how to model this problem?
observations:
either == or !=

if all equations are == then fine 
if all eqautions are != also fine (given no such a!=a)

so basically, when a!=b.. and if a is already a==b.. then it is bummer
so I guess I can process == first.. 

then I process != 
give a try and see where it crashes

so as you can see, there are at most 26 variables. which provides me the convience to construct roots[]
"""


from typing import List


class Solution:
    def equationsPossible(self, equations: List[str]) -> bool:
        roots = list(range(26))

        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]
        
        def union(x,y):
            roots[find(x)] = roots[find(y)]

        for eq in equations:
            if eq[1:3] == '==':
                v1,v2 = ord(eq[0])-ord('a'), ord(eq[3])-ord('a')
                if find(v1) != find(v2):
                    union(v1,v2)

        for eq in equations:
            if eq[1:3] == '!=':
                v1, v2 = ord(eq[0])-ord('a'), ord(eq[3])-ord('a')
                if v1==v2 or find(v1) == find(v2):
                    return False
        
        return True

"""
Runtime: 80 ms, faster than 32.10% of Python3 online submissions for Satisfiability of Equality Equations.
Memory Usage: 13.9 MB, less than 93.58% of Python3 online submissions for Satisfiability of Equality Equations.
"""