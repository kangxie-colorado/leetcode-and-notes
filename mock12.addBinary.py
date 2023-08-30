class Solution:
    def addBinary(self, a: str, b: str) -> str:
        i,j = len(a)-1, len(b)-1
        c = 0
        res = []
        while i>=0 and j>=0:
            s = int(a[i]) + int(b[j]) + c
            res.append(str(s % 2))
            c = s // 2
            i,j = i-1,j-1
        
        a,i = (a,i) if i>=0 else (b,j)
        while i>=0:
            s  = int(a[i]) + c
            res.append(str(s % 2))
            c = s // 2
            i-=1
        
        if c>0:
            res.append(str(c))
        
        res.reverse()
        return "".join(res)
        
if __name__ == '__main__':
    s = Solution()
    print(s.addBinary(a = "11", b = "1"))
    print(s.addBinary(a = "1010", b = "1011"))

        