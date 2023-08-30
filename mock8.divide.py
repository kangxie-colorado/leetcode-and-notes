"""
for a moment, I don't know how to do
because nore multiplication/division/mod can be used

I used substraction
then I came to realize that I could use the <<
"""

class Solution:
    def divide(self, dividend: int, divisor: int) -> int:
        neg = False
        if (dividend>0 and divisor<0) or (dividend<0 and divisor>0):
            neg = True
        
        dividend = abs(dividend)
        divisor = abs(divisor)
        
        res = 0
        while dividend >= divisor:
            dividend -= divisor
            res += 1
        
        return -res if neg else res

class Solution:
    def divide(self, dividend: int, divisor: int) -> int:
        neg = 1
        if (dividend>0 and divisor<0) or (dividend<0 and divisor>0):
            neg = -1
        
        dividend = abs(dividend)
        divisor = abs(divisor)

        res = 0

        while dividend >= divisor:
          shift = 0
          while divisor<<shift <= dividend:
              shift += 1
          res += 1<<(shift-1)
          dividend -= divisor<<(shift-1)
        
        res *= neg
        if res > (1<<31) - 1:
            res = (1<<31) - 1
        if res < -1<<31:
            res = -1<<31
        return res


if __name__ == '__main__':
    s = Solution()
    # print(s.divide(10,3))
    # print(s.divide(10,-3))
    # print(s.divide(7,-3))
    print(s.divide(-2147483648, -1))
    print(s.divide(-2147483648, 1))
