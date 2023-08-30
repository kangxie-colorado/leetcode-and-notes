"""
move left/right first, because of z
so it is moving y first

I was in my own mind trap of moving x 
"""

class Solution:
    def alphabetBoardPath(self, target: str) -> str:
        x,y = 0,0
        res = ""

        for c in target:
            ordc = ord(c) - ord('a')
            nx,ny = ordc//5, ordc%5
            if x==nx and y==ny:
                res += '!'
                continue

            run = ''
            if x == 5:
                x -= 1
                run = 'U'

            xmove = 'U' if nx<x else 'D'
            ymove = 'L' if ny<y else 'R'

            run += ymove*abs(ny-y) + xmove*abs(nx-x)  + '!'
            res = f"{res}{run}"
            x,y = nx,ny
        
        return res

