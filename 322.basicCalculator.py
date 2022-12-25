"""
https://leetcode.com/problems/basic-calculator/?envType=study-plan&id=programming-skills-iii

at first I thought of using stack
maintain a series of stack.. current stack will reduce to a single value and get applied to parent run
it should be doable.. 

I recently did something similar to that

but seeing this 
s consists of digits, '+', '-', '(', ')', and ' '.

making it a bit easier?
maybe I can just remove all the () and do a plain calculation 
however the unary '-' complicates things up...

let me see
probably I still return to that stack-based way?

or actually I can find the matching () and use what is in the middle to the calculation
"""


class Solution:
    def calculate(self, s: str) -> int:

        def myEval(l):
            toCalS = []
            for e in l:
                if type(e) is list:
                    toCalS.append(myEval(e))
                else:
                    if e not in '+-':
                        toCalS.append(int(e))
                    else:
                        toCalS.append(e)
            
            i=0
            nums = []
            op = ''
            while i<len(toCalS):

                c = toCalS[i]
                if i==0 and c=='-':
                    nums.append(-toCalS[i+1])
                    i+=1
                else:
                    if type(c) is int:
                        nums.append(c)
                        if len(nums) > 1 and op:
                            nums = [nums[0]+nums[1],
                                    ] if op == '+' else [nums[0]-nums[1], ]
                    else:
                        op = c 

                i += 1
            return nums[0]



        s = '(' + s + ')'

        # keep curr run at the top of stack
        stack = []
        i=0
        while i<len(s):
            c = s[i]
            if c == '(':
                curr = []
                stack.append(curr)
            elif c == ')':
                run = stack.pop()
                if stack:
                    curr = stack[-1]
                    curr.append(run)
            elif c == ' ':
                ...
            else:
                if c.isdigit():
                    j = i+1
                    while j<len(s) and s[j].isdigit():
                        c += s[j]
                        j+=1
                    i = j-1
                curr.append(c)
            i+=1
        print(curr)
        return int(myEval(curr))

"""
Runtime: 189 ms, faster than 49.94% of Python3 online submissions for Basic Calculator.
Memory Usage: 18 MB, less than 9.40% of Python3 online submissions for Basic Calculator.

there should be a place in the parsing code to actually calculate the number from curr run
because when a current run finishes.. it has to be and can be evaluated into a num
"""


class Solution:
    def calculate(self, s: str) -> int:

        def myEval(l):
            i = 0
            nums = []
            op = ''
            while i < len(l):
                c = l[i]
                if i == 0 and c == '-':
                    # it must be followed by a number
                    nums.append(-l[i+1])
                    i += 1
                else:
                    if type(c) is int:
                        nums.append(c)
                        if len(nums) > 1 and op:
                            nums = [nums[0]+nums[1],
                                    ] if op == '+' else [nums[0]-nums[1], ]
                    else:
                        op = c

                i += 1
            return nums[0]

        s = '(' + s + ')'

        # keep curr run at the top of stack
        stack = []
        i = 0
        while i < len(s):
            c = s[i]
            if c == '(':
                curr = []
                stack.append(curr)
            elif c == ')':
                num = myEval(stack.pop())

                if stack:
                    curr = stack[-1]
                    curr.append(num)
            elif c == ' ':
                ...
            else:
                if c.isdigit():
                    j = i+1
                    while j < len(s) and s[j].isdigit():
                        c += s[j]
                        j += 1
                    i = j-1
                    c = int(c)
                curr.append(c)
            i += 1
        # print(curr)
        return int(myEval(curr))

"""
Runtime: 175 ms, faster than 55.81% of Python3 online submissions for Basic Calculator.
Memory Usage: 15.5 MB, less than 33.29% of Python3 online submissions for Basic Calculator.
"""

if __name__ == '__main__':
    s = Solution()
    print(s.calculate("2147483647"))
    print(s.calculate("1-(     -2)"))
    print(s.calculate("1-(-(-(-(-(1)))))"))
    print(s.calculate("(1+(4+5+2)-3)+(6+8)"))
