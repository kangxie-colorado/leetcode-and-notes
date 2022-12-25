"""
https://leetcode.com/problems/string-to-integer-atoi/

so many edge cases..
need careful programming

"""


class Solution:
    def myAtoi(self, s: str) -> int:
        i = 0
        minInt, maxInt = -2147483648, 2147483647
        maxIntStr = "2147483647"
        s = s.strip()
        if not s or s[0] not in '+-0123456789':
            return 0

        def biggerThanMax(num):
            num = num.lstrip('0')
            if len(num) == len(maxIntStr):
                return num > maxIntStr
            return len(num) > len(maxIntStr)

        while i < len(s):
            c = s[i]
            if c in '+-' or c.isdigit():
                num = c if c.isdigit() else ""
                j = i+1
                while j < len(s) and s[j].isdigit():
                    num += s[j]
                    j += 1
                j -= 1

                if len(num) == 0:
                    return 0
                sign = -1 if c == '-' else 1

                if biggerThanMax(num):
                    return minInt if sign == -1 else maxInt
                else:
                    return sign*int(num)

            i += 1

        return 0


""""
Runtime: 39 ms, faster than 86.79% of Python3 online submissions for String to Integer (atoi).
Memory Usage: 14 MB, less than 29.42% of Python3 online submissions for String to Integer (atoi).
"""


class Solution:
    def myAtoi(self, s: str) -> int:
        i = 0
        minInt, maxInt = -2147483648, 2147483647
        maxIntStr = "2147483647"
        s = s.strip()
        if not s or s[0] not in '+-0123456789':
            return 0

        def biggerThanMax(num):
            num = num.lstrip('0')
            if len(num) == len(maxIntStr):
                return num > maxIntStr
            return len(num) > len(maxIntStr)

        while i < len(s):
            c = s[i]
            if c in '+-' or c.isdigit():
                sign = -1 if c == '-' else 1
                num = c if c.isdigit() else ""
                j = i+1
                while j < len(s) and s[j].isdigit():
                    num += s[j]
                    if len(num) >= len(maxIntStr) and biggerThanMax(num):
                        return minInt if sign == -1 else maxInt
                    j += 1
                j -= 1

                if len(num) == 0:
                    return 0
                return sign*int(num)

            i += 1

        return 0

"""
Runtime: 29 ms, faster than 98.59% of Python3 online submissions for String to Integer (atoi).
Memory Usage: 14 MB, less than 29.42% of Python3 online submissions for String to Integer (atoi).
"""