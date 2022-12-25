"""
https://leetcode.com/problems/expression-add-operators/?envType=study-plan&id=programming-skills-iii


This is a difficult problem!!
I was thinking how to brute force

e.g. for 10 digits... 
then adding an op (+-*) between digit.. 9 of them, 3**9
then using 8 ops.. 3**8
then...

but here.. when using 7 ops.. that means one operand can be 3; or two of them can be 2 and 2
this quickly complicated things up... so I don't even know how to brute force

then watched Hua Hua's video.. the first simplification is treat "" (adding nothing as an operator)
so there are 4 ops: +/-/*/""
so here comes 4**(n-1).. for each pos.. the rest is like 4**(n1-1).. 
so kind of O(n * 4^(n-1))

the idea is to keep states as follow
i: the index of the input string being processed
prev: the last segment, 1+2 => 2; 1-2 => -2... 
curr: the current evaluation.. this is to save the trouble of doing a final eval at the end of string building

the technique to process * is 
it will be bound into prev, prev*=new_num, and curr will be calculated by curr-prev + prev*new_num

at each i, the next number can take 1 digits, 2 digits and up to all the digits left.. 
so "" operator is kind of implicitly executed 

"""



from typing import List



class Solution:
    def addOperators(self, num: str, target: int) -> List[str]:
        # try printing out all the possibilities        
        def dfs(i, sofar):
            if i>=len(num):
                # print(sofar)
                return 
            
            for j in range(i, len(num)):
                if i==0:
                    dfs(j+1, [num[i:j+1]])
                    continue
                dfs(j+1, sofar+['+']+[num[i:j+1]])
                dfs(j+1, sofar+['-']+[num[i:j+1]])
                dfs(j+1, sofar+['*']+[num[i:j+1]])
        
        dfs(0, [])

    def addOperators(self, num: str, target: int) -> List[str]:
        # try using eval() to see how far it goes
        """
        "3456237490"
        9191
        it take 5s

        then 
        20 / 23 test cases passed. failed here
        "9999999999"
        1409865409
        """
        output = []
        def dfs(i, sofar):
            if i >= len(num):
                res = eval("".join(sofar))
                # print(sofar, res)
                if res == target:
                    output.append("".join(sofar))

                return

            for j in range(i, len(num)):
                if i == 0:
                    dfs(j+1, [num[i:j+1]])
                else:
                    dfs(j+1, sofar+['+']+[num[i:j+1]])
                    dfs(j+1, sofar+['-']+[num[i:j+1]])
                    dfs(j+1, sofar+['*']+[num[i:j+1]])

                if num[i] == '0':
                    # 0 can go itself.. 
                    # but 01 02 or 013 ... cannot go
                    # so the loop must break now
                    break

        dfs(0, [])
        return output

    def addOperators(self, num: str, target: int) -> List[str]: # ~1050ms 
        # now let us try to build in the partitial evaluation 
        output = []

        def dfs(i, sofar, prev, res):
            if i >= len(num):
                print(sofar, res)
                if res == target:
                    output.append("".join(sofar))

                return

            for j in range(i, len(num)):
                n = int(num[i:j+1])
                if i == 0:
                    dfs(j+1, [num[i:j+1]], n, n)
                else:
                    # notice prev(term) is on the pespective of next call
                    # and for '-', it should be -n
                    dfs(j+1, sofar+['+']+[num[i:j+1]], n, res+n)
                    dfs(j+1, sofar+['-']+[num[i:j+1]], -n, res-n) 
                    dfs(j+1, sofar+['*']+[num[i:j+1]], prev*n, res-prev+prev*n)

                if num[i] == '0':
                    # 0 can go itself..
                    # but 01 02 or 013 ... cannot go
                    # so the loop must break now
                    break

        dfs(0, [], 0, 0)
        return output


    def addOperators(self, num: str, target: int) -> List[str]:
        # looks no reason to keep the so far around
        output = []

        def dfs(i, sofar, prev, res):
            if i >= len(num):
                print(sofar, res)
                if res == target:
                    output.append(sofar)

                return

            for j in range(i, len(num)):
                n = int(num[i:j+1])
                if i == 0:
                    dfs(j+1, num[i:j+1], n, n)
                else:
                    # notice prev(term) is on the pespective of next call
                    # and for '-', it should be -n
                    dfs(j+1, f"{sofar}+{num[i:j+1]}", n, res+n)
                    dfs(j+1, f"{sofar}-{num[i:j+1]}", -n, res-n)
                    dfs(j+1, f"{sofar}*{num[i:j+1]}", prev*n, res-prev+prev*n)

                if num[i] == '0':
                    # 0 can go itself..
                    # but 01 02 or 013 ... cannot go
                    # so the loop must break now
                    break

        dfs(0, "", 0, 0)
        return output

"""
Runtime: 831 ms, faster than 90.44% of Python3 online submissions for Expression Add Operators.
Memory Usage: 14.7 MB, less than 46.71% of Python3 online submissions for Expression Add Operators.

so manipulate string is a bit faster?
"""

print(Solution().addOperators("123", 6))
