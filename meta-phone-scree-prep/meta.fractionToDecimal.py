"""
given a denominator D, any numerator N,
apply N%D will result in a remaind (0 to D-1)

so when the remainder re-appears, the result/remain will begin to repeat
so this would be to go thru and monitor the repeating remainder 

but when to start count, I'll see until the numerator is bigger than denominator 

"""

class Solution:
    def fractionToDecimal(self, numerator: int, denominator: int) -> str:
        if numerator % denominator == 0:
           return str(numerator//denominator)
        
        intPart = int(abs(numerator)/abs(denominator))
        res = f"{intPart}."

        remainder = (abs(numerator) % abs(denominator))
        sign = ""
        if numerator//abs(numerator) != denominator//abs(denominator):
           remainder = (remainder + abs(denominator)) % abs(denominator)
           sign = '-'
        
        denominator = abs(denominator)
        numerator = remainder * 10
        remainders = {}
        repating = ""

        while True:
          res += str(numerator//denominator)
          numerator = numerator % denominator
          if numerator == 0:
             break
          
          if numerator in remainders:
             repating = res[remainders[numerator]:len(res)]
             res = res[:remainders[numerator]] + f"({repating})"
             break
          
          # here is a bit tricky, the remainder will be pointing to next result number
          # e.g. 4/13, 
          # starting 40 13 -> 3 1; here 1 as reminader will decide next result to be 0
          # so it points to next result's position which will be the length of res
          # cont 10 13 -> 0 10; 10 will decide next result to be 7, also at length of res
          # 100 13 -> 7 9... 
          # so on so forth.. 
          # also this problem is not very clear that 
          # 1/3 can be accepted as 0.(3) or 0.3(3) or o.333(3)
          remainders[numerator] = len(res)
          
          while numerator*10 < denominator:
              res += '0'
              numerator *= 10
              remainders[numerator] = len(res)
              
          numerator *= 10
        
        return f"{sign}{res}"
    
if __name__ == "__main__":
   s = Solution()
   print(s.fractionToDecimal(-50,8))
   print(s.fractionToDecimal(-4,-2))
   print(s.fractionToDecimal(1,-2))
   print(s.fractionToDecimal(1,2))
   print(s.fractionToDecimal(4,13))
   print(s.fractionToDecimal(1,3))
   print(s.fractionToDecimal(1,6))
        

