"""
for each postion there are 4 choices.
nothing, +, -, *

so I can just brute force? 10**4, yeah that is possible
especially in the phone screen.. we can do that

maybe we can go from behind to front, so that we could make it sub-problem

because if you go from front to back, 1-, 1+, you cannot decide the value the later part should evaluate to
but from behind -1, then it should be target + 1
however, if *2, then you still don't know...

so okay.. looks like only the brute force search can do...
"""

from typing import List


class Solution:
    def addOperators(self, num: str, target: int) -> List[str]:
        def comb(ops):
            # just interleave two array
            ops += [""]
            return "".join([n+op for n,op in zip(num,ops)])
        
        res = []
        def f(idx, ops):
            """
            idx is the insert position can only be 1 to len(num)-1
            nah.. the num is changing.. 
            nah.. I don't need to change it
            keep it separately, and combine them to eval
            """

            if idx == len(num):
                # do combine and eval
                cand = comb(ops)
                if eval(cand) == target:
                    res.append(cand)
                return 
            
            for op in ["", "+", "-", "*"]:
                if num[idx-1] == '0' and op == "":
                    continue
                f(idx+1, ops+[op])

        f(1,[])            
        return res
    
"""
there is a bug in this
            
                if num[idx-1] == '0' and op == "":
                    continue
                    
if the operand is 10, for the incoming 0, I will not have the comb for 100 but will alway skip
so I should look one more step back, if num[idx-1] is not 0... then I can attach

^ still not right

the better criterea should be from the ops.. let me see
if my last number is 0, and last operator is "", it can be otherwise, it cannot
"""

class Solution:
    def addOperators(self, num: str, target: int) -> List[str]:
        def comb(ops):
            # just interleave two array
            ops += [""]
            return "".join([n+op for n,op in zip(num,ops)])
        
        res = []
        def f(idx, ops):
            """
            idx is the insert position can only be 1 to len(num)-1
            nah.. the num is changing.. 
            nah.. I don't need to change it
            keep it separately, and combine them to eval
            """

            if idx == len(num):
                # do combine and eval
                cand = comb(ops)
                if eval(cand) == target:
                    res.append(cand)
                return 
            
            for op in ["", "+", "-", "*"]:
                if idx==1 and num[0] == '0' and op == "":
                    continue
                if num[idx-1] == '0' and op == "" and ops[-1]!="":
                    continue
                f(idx+1, ops+[op])

        f(1,[])            
        return res

if __name__ == '__main__':
    s = Solution()
    print(s.addOperators(num = "010", target = 0))
    # print(s.addOperators(num = "1005", target = 5))
    # print(s.addOperators(num = "105", target = 5))
    # print(s.addOperators(num = "123", target = 6))
    # print(s.addOperators(num = "232", target = 8))
                    