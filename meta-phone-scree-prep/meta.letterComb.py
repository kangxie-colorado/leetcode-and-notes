from functools import cache
from typing import List


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        digitCharMap = {"2": "abc", "3": "def", "4": "ghi", "5":"jkl", "6":"mno", "7":"pqrs", "8":"tuv", "9":"wxyz"}
        
        @cache
        def f(idx):
            if idx == len(digits):
                return []
            
            res = []
            digit = digits[idx]
            for d in digitCharMap[digit]:
                left = [d]
                right = f(idx+1)
                for l in left:
                    for r in right:
                        res.append(l+r)
            
            return res

        return f(0)

if __name__ == '__main__'          :
    s = Solution()
    print(s.letterCombinations('2'))
            