class Solution:
    def removeDuplicates(self, s: str, k: int) -> str:
        res = [""]*len(s)
        i = 0

        for j in range(len(s)):
            res[i] = s[j]
            if i>=(k-1) and res[i-k+1:i+1]==[res[i]]*k:
                i-=k 
            i+=1
        
        return "".join(res[:i])


class Solution:
    def removeDuplicates(self, s: str, k: int) -> str:
        stack = []
        for c in s:
            if stack and stack[-1][0] == c:
                if stack[-1][1] == k-1:
                    stack.pop()
                else:
                    stack[-1][1] += 1
            else:
                stack.append([c,1])
        
        res = "".join(c*n for c,n in stack)
        return res
            
              

if __name__ == "__main__":
    s = Solution()
    print(s.removeDuplicates(s = "deeedbbcccbdaa", k = 3))