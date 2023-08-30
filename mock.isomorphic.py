from collections import defaultdict


class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        
        def f(src, tgt):
            charPos = defaultdict(list)
            for i,c in enumerate(src):
                charPos[c].append(i)
            
            for c,l in charPos.items():
                if len(l) == 1:
                    continue
                
                ref = tgt[l[0]]
                for idx in l:
                    if tgt[idx] != ref:
                        return False
            
            return True
        
        return f(s,t) and f(t,s)
    

if __name__ == '__main__':
    s = Solution()
    print(s.isIsomorphic("badc", "baba"))