class Solution:
    def decodeString(self, s: str) -> str:
        
        stack = []
        pairs = {} # left-idx: (right-idx, multiplier-in-str)
        # get the pair-idx of []
        for i,c in enumerate(s):
            if c not in '[]':
                continue
            if c == '[':
                stack.append(i)
            else:
                l = stack.pop()
                mIdx = l-1
                m = ""
                while mIdx>=0 and s[mIdx].isdigit():
                    m = f"{s[mIdx]}{m}"
                    mIdx -= 1
                pairs[l] = (i, m)
        
        def f(start,end):
            subStr = s[start:end]
            if '[' not in subStr:
                return subStr
            
            lIdx = subStr.index('[') + start
            rIdx,mul = pairs[lIdx]

            return subStr[:lIdx-start-len(mul)] + f(lIdx+1, rIdx)*int(mul) + f(rIdx+1, end)
      
        return f(0,len(s))
  
if __name__ == '__main__':
    s = Solution()
    print(s.decodeString(s = "3[a]2[bc]"))
    print(s.decodeString(s = "3[a2[c]]"))
    print(s.decodeString(s = "2[abc]3[cd]ef"))
            
