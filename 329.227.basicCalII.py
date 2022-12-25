"""
https://leetcode.com/problems/basic-calculator-ii/?envType=study-plan&id=programming-skills-iii

now, think it as term?

"""


class Solution:
    def calculate(self, s: str) -> int:
        i = 0
        prev = res = 0
        op = '+'
        while i<len(s):
            c = s[i]

            if c == ' ':
                ...
            elif c.isdigit():
                num = c
                j = i+1
                while j<len(s) and s[j].isdigit():
                    num += s[j]
                    j+=1
                j-=1
                i=j
                num = int(num)
                if op == '+':
                    prev = num
                    res += num
                if op == '-':
                    prev = -num
                    res -= num
                if op == '*':
                    res = res - prev + prev*num
                    prev *= num
                if op == '/':
                    res = res - prev + int(prev/num)
                    prev = int(prev/num)
            else:
                op = c
            i+=1
            
        return res

""""
Runtime: 202 ms, faster than 54.67% of Python3 online submissions for Basic Calculator II.
Memory Usage: 16.2 MB, less than 42.58% of Python3 online submissions for Basic
"""
                

""""
surprise

>>> int(-3/2)
-1
>>> -3//2
-2
"""


class Solution:
    def calculate(self, s: str) -> int:
        s.replace(" ", "")

        def f(i,op, prev,res):
            if i==len(s):
                return res
            if s[i] == ' ':
                return f(i+1, op, prev, res)            
            if s[i] in "+-*/":
                op = s[i]
                return f(i+1, op, prev, res)
            
            num = 0
            while i<len(s) and s[i].isdigit():
                num = num*10 + int(s[i])
                i+=1
            
            if op == '+': 
                return f(i, op, num, res+num)
            if op == '-':
                return f(i, op, -num, res-num)
            if op == '*':
                return f(i, op, prev*num, res-prev+prev*num)
            if op == '/':
                return f(i, op, int(prev/num), res-prev+int(prev/num))

        return f(0, '+', 0, 0)
"""
Runtime: 367 ms, faster than 20.61% of Python3 online submissions for Basic Calculator II.
Memory Usage: 343.6 MB, less than 5.26% of Python3 online submissions for Basic Calculator II.

why so many memory??
"""

if __name__ == '__main__':
    S  = Solution()
    print(S.calculate('14-3/2'))