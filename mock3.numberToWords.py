"""
looks like every 3 digits can be treated separately
"""

class Solution:
    def numberToWords(self, num: int) -> str:
        if not num:
            return "Zero"
        units = ["", "Thousand", "Million", "Billion"]
        teens = ["", "Eleven", "Twelve", "Thirteen", "Fourteen","Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
        tens = ["", "Ten", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
        digits = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]

        # translate num < 1000
        def translate3(num, unitIdx):
            res = ""
            # look at the lower 2 digits and the hundred digit
            hundreds = digits[num // 100]
            if hundreds:
                res = f"{hundreds} Hundred"
            
            lower2 = num % 100
            if lower2 % 10 == 0: # tens or 0
                tenUnit = tens[lower2 // 10]
                if tenUnit:
                    res = f"{res} {tenUnit}"
            elif 10<lower2 < 20:
                res = f"{res} {teens[lower2-10]}"
            elif lower2<10:
                res = f"{res} {digits[lower2-0]}"
            else:
                tenUnit = tens[lower2//10]
                digitUnit = digits[lower2%10]
                res = f"{res} {tenUnit} {digitUnit}"
            
            if res:
              res = f"{res} {units[unitIdx]}"
            return res

        res = ""
        idx = 0 
        while num:
            lower3 = num % 1000
            res = f"{translate3(lower3, idx)} {res}" 
            num //= 1000
            idx += 1
        
        return "".join(res.split())
        
                
if __name__ == '__main__':
    s = Solution()
    print(s.numberToWords(123))
    print(s.numberToWords(12345))
    print(s.numberToWords(1234567))
