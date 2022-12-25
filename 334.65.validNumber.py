"""
https://leetcode.com/problems/valid-number/?envType=study-plan&id=programming-skills-iii

basically this can divide and conquer

exist e or not e
before e and behind e
"""


class Solution:
    def isNumber(self, s: str) -> bool:
        def validDecimal(decimal):
            if not decimal:
                return False
            

            if decimal[0] in '+-':
                return validDecimal(decimal[1:])
            elif decimal[0] == '.':
                return validInteger(decimal[1:], pure=True)
            else:
                split = len(decimal)
                for i, c in enumerate(decimal):
                    if c == '.':
                        split = i
                        break

                if split < len(decimal):
                    if decimal[:split] and decimal[split+1:]:
                        return validInteger(decimal[:split]) and validInteger(decimal[split+1:], pure=True)    
                    elif not decimal[:split] and not decimal[split+1:]:
                        return False
                    else:
                        if decimal[split+1:]:
                            return validInteger(decimal[split+1:], pure=True)
                        else:
                            return validInteger(decimal[:split])
                return validInteger(decimal)

        def validInteger(integer, pure=False):
            if not integer:
                return False

            # now there is no letters.. but could be '.'
            if integer[0] in '+-':
                if pure:
                    return False
                return integer[1:] and all([c.isdigit() for c in integer[1:]])
            else:
                return all([c.isdigit() for c in integer])

        split = len(s)
        for i, c in enumerate(s):
            if c not in 'Ee+-.' and not c.isdigit():
                return False
            if c in 'Ee':
                split = i
                break

        if split < len(s):
            return validDecimal(s[:split]) and validInteger(s[split+1:])

        return validDecimal(s)

"""
Runtime: 46 ms, faster than 71.90% of Python3 online submissions for Valid Number.
Memory Usage: 14 MB, less than 5.87% of Python3 online submissions for Valid Number.

Runtime: 33 ms, faster than 94.55% of Python3 online submissions for Valid Number.
Memory Usage: 13.9 MB, less than 29.67% of Python3 online submissions for Valid Number.
"""


class Solution:
    def isNumber(self, s: str) -> bool:
        def validDecimal(decimal):
            if not decimal:
                return False

            if decimal[0] in '+-':
                return validDecimal(decimal[1:])
            elif decimal[0] == '.':
                return validInteger(decimal[1:], pure=True)
            else:
                parts = decimal.split('.')
                if len(parts) > 2:
                    return False

                if len(parts) == 2:
                    if parts[0] or parts[1]:
                        if parts[0] and parts[1]:
                            return validInteger(parts[0]) and validInteger(parts[1], pure=True)
                        elif parts[1]:
                            return validInteger(parts[1], pure=True)
                        else:
                            return validInteger(parts[0])
                    else:
                        return False
                return validInteger(decimal)

        def validInteger(integer, pure=False):
            if not integer:
                return False

            # now there is no letters.. but could be '.'
            if integer[0] in '+-':
                if pure:
                    return False
                return validInteger(integer[1:], pure=True)
            else:
                return all([c.isdigit() for c in integer])
        
        import re
        parts = re.split('e|E', s)
        if len(parts) > 2:
            return False

        if len(parts) == 2:
            return validDecimal(parts[0]) and validInteger(parts[1])

        return validDecimal(s)

"""
Runtime: 31 ms, faster than 97.11% of Python3 online submissions for Valid Number.
Memory Usage: 14 MB, less than 5.87% of Python3 online submissions for Valid Number.
"""

if __name__ == '__main__':
    s = Solution()
    print(s.isNumber('.-4'))