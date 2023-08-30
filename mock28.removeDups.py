class Solution:
    def removeDuplicates(self, s: str) -> str:

        def dupIdx(s):
            i=0
            for c1,c2 in zip(s,s[1:]):
                if c1==c2:
                    return i
                i+=1
            return -1
        
        dup = dupIdx(s)
        while dup!=-1:
            s = s[:dup] + s[dup+2:]
            dup = dupIdx(s)
        
        return s

"""
aha... this is an easy problem
when you think in the wrong direction you would never figure it out

if they give you a hint, do think hard...

"""

class Solution:
    def removeDuplicates(self, s: str) -> str:
        stack = []
        for c in s:
            if stack and stack[-1] == c:
                stack.pop()
            else:
                stack.append(c)
        return "".join(stack)

"""
https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string/discuss/294893/JavaC%2B%2BPython-Two-Pointers-and-Stack-Solution

the first solution is pretty cool
it can deal with three duplicates, or more

maybe no such problem but it is still kind of cool
there is!!!

https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string-ii/
so yeah, such a cool problem


"""


class Solution:
    def removeDuplicates(self, s: str) -> str:
        res = [""]*len(s)
        i = 0
        for j in range(len(s)):
            res[i] = s[j]
            if i>0 and res[i]==res[i-1]:
                i-=2
            i+=1
        return "".join(res[:i])

                    
if __name__ == '__main__':
    s = Solution()
    print(s.removeDuplicates('abbaca'))