from typing import List


class Solution:
    def expand(self, s: str) -> List[str]:
        choices = []
        stack = []

        for i,c in enumerate(s):
            if c not in '{}':
                if not stack:
                    choices.append([c])
                continue
            
            if c == '{':
                stack.append(i)
            else:
                i1 = stack.pop()
                subStr = s[i1+1:i]
                choice = subStr.split(',')
                choices.append(sorted(choice))
        
        def f(idx):
            if idx == len(choices):
                return [[]]
            
            res = []
            for c in choices[idx]:
                for subC in f(idx+1):
                  res.append([c] + subC)
            
            return res  
        
        res = []
        for choice in f(0):
            res.append("".join(choice))
        
        return res

if __name__ == "__main__":
    s =Solution()
    print(s.expand(s = "{a,b}c{d,e}f"))

