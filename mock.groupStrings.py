from collections import defaultdict
from typing import List


class Solution:
    def groupStrings(self, strings: List[str]) -> List[List[str]]:
        strLenMap = defaultdict(list)
        for s in strings:
            strLenMap[len(s)].append(s)

        res = []
        for l,strs in strLenMap.items():
            if l == 1:
                res.append(strs)
                continue
            used = set()
            for i in range(len(strs)):
                if strs[i] in used:
                    continue
                run = [strs[i]]
                for j in range(i+1,len(strs)):
                    if strs[j] in used:
                        continue
                    delta = (ord(strs[j][0])-ord(strs[i][0])+26)%26
                    sameSequence = True
                    for k in range(1, len(strs[i])):
                        if (ord(strs[j][k])-ord(strs[i][k])+26)%26 != delta:
                            sameSequence = False
                            break 
                        
                    if sameSequence:
                        run.append(strs[j])
                        used.add(strs[j])
                res.append(run)
          
        return res
                
    
        
        