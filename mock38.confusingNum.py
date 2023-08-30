class Solution:
    def confusingNumberII(self, n: int) -> int:
        valid = {
            0:0,
            1:1,
            6:9,
            8:8,
            9:6
        }
        res = 0

        def rotate180(num):
            rotated = 0
            while num:
                d = num%10
                rotated = rotated*10 + valid[d]
                num // 10
            return rotated

        def backtrack(num):
            if num>n:
                return
            
            nonlocal res
            res += (num != rotate180(num))

            for next in valid:
                if num==0 and next==0:
                    continue        
                backtrack(num*10+next)
        
        backtrack(0)
        return res