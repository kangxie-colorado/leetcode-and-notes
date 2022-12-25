"""
https://leetcode.com/problems/basic-calculator-iii/?envType=study-plan&id=programming-skills-iii

this is just a combination problem of basic calculator I and II
"""


class Solution:
    def calculate(self, s: str) -> int:
        def myEval(run):
            stack = []
            sign = 1
            op = '+'
            for e in run:
                if type(e) is str and e in '+-*/':
                    op = e
                    sign = -1 if op == '-' else 1
                else:
                    if op in '+-':
                        stack.append((sign, e))
                    else:
                        lastSign, lastNum = stack.pop()
                        if op == '*':
                            stack.append((lastSign, lastNum*e))
                        if op == '/':
                            stack.append((lastSign, int(lastNum/e)))

            res = 0
            for s, e in stack:
                res += s*e

            return res

        s = f'({s})'
        stack = []
        i = 0
        curr = None
        while i < len(s):
            c = s[i]
            if c == ' ':
                ...
            elif c == '(':
                curr = []
                stack.append(curr)
            elif c == ')':
                num = myEval(stack.pop())
                if stack:
                    curr = stack[-1]
                    curr.append(num)
            elif c in '+-*/':
                curr.append(c)
            else:
                num = int(c)
                j = i+1
                while j < len(s) and s[j].isdigit():
                    num = num*10 + int(s[j])
                    j += 1
                j -= 1
                i = j
                curr.append(num)
            i += 1

        return num

"""
Runtime: 48 ms, faster than 76.83% of Python3 online submissions for Basic Calculator III.
Memory Usage: 13.9 MB, less than 94.59% of Python3 online submissions for Basic Calculator III.
"""


if __name__ == '__main__':
    S  = Solution()
    print(S.calculate('6-4/2'))