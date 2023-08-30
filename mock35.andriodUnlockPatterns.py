from functools import cache


class Solution:
    def numberOfPatterns(self, m: int, n: int) -> int:
        pairs = {
            (1,3),(3,1),(4,6),(6,4),(7,9),(9,7),(1,7),(7,1),(2,8),(8,2),(3,9),(9,3),(1,9),(9,1),(3,7),(7,3)
        }
        
        @cache
        def f(i, last, selections):
            if i==0:
                return 1
            
            res = 0
            for next in range(1,10):
                if selections & (1<<next):
                    continue
                
                # only route to discard is when there is a middle number and not in selections

                if (last,next) in pairs and not (selections & (1<<((last+next)//2))) :
                    continue
                
                res += f(i-1, next, selections | (1<<next))

            return res
        
        def g(num):
            res = 0
            for start in range(1,10):
                res += f(num-1, start, 1<<start) # careful!!! you alreays used one selection with this drive
            return res
        
        res = 0
        for k in range(m,n+1):
            res += g(k)
        return res
"""    

this is the tricky part
        def g(num):
            res = 0
            for start in range(1,10):
                res += f(num-1, start, 1<<start) # careful!!! you alreays used one selection with this drive
            return res
maybe can be replaced by 
        def g(num):
            res = 0
            f(0,0,0) 
              ^ because 0 doesn't exist so will not impact
"""

class Solution:
    def numberOfPatterns(self, m: int, n: int) -> int:
        pairs = {
            (1,3),(3,1),(4,6),(6,4),(7,9),(9,7),(1,7),(7,1),(2,8),(8,2),(3,9),(9,3),(1,9),(9,1),(3,7),(7,3)
        }
        
        @cache
        def f(i, last, selections):
            if i==0:
                return 1
            
            res = 0
            for next in range(1,10):
                if selections & (1<<next):
                    continue
                
                # only route to discard is when there is a middle number and not in selections

                if (last,next) in pairs and not (selections & (1<<((last+next)//2))) :
                    continue
                
                res += f(i-1, next, selections | (1<<next))

            return res
        
        res = 0
        for k in range(m,n+1):
            res += f(k,0,0)
        return res

"""
then there is no need to have the function g(n)

"""

if __name__ == '__main__':
    
    s = Solution()
    print(s.numberOfPatterns(1,1))
    print(s.numberOfPatterns(1,3))