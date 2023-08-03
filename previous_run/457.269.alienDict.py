"""
https://leetcode.com/problems/alien-dictionary/?envType=study-plan&id=graph-ii

okay.. shitty sleep last night.. 
but hope I can get pass this one

I know how to do it after all

compare between each words.. establish some order 
then bfs
"""


from collections import defaultdict, deque
import queue
from typing import List


class Solution:
    def alienOrder(self, words: List[str]) -> str:
        graphs = defaultdict(set)
        before = defaultdict(set)
        
        for i in range(len(words)):
            for j in range(i+1, len(words)):
                w1,w2 = words[i], words[j]
                for c1,c2 in zip(w1,w2):
                    if c1!=c2:
                        graphs[c1].add(c2)
                        graphs[c2].add(c1)
                        before[c2].add(c1)
                        break
        
        incomingLinks = [0]*26
        bfsQ = deque()
        for c in graphs:
            incomingLinks[ord(c)-ord('a')] = len(before[c])
            if incomingLinks[ord(c)-ord('a')] == 0:
                bfsQ.append(c)
        
        res = []
        while bfsQ:
            sz = len(bfsQ)
            while sz:
                c = bfsQ.popleft()
                res.append(c)

                for nextC in graphs[c]:
                    incomingLinks[ord(nextC)-ord('a')]-=1
                    if incomingLinks[ord(nextC)-ord('a')] == 0:
                        bfsQ.append(nextC)
                sz-=1
        return "".join(res)

"""
["z","z"]
failed here.. 

experiment it 
["zy","zx"] expected "xyz", i got "yz

so it looks when there is no relationship.. 
just append to the back

so I change my algorithm as follow
    - still deal with the relative chars first
    - for non-related.. append to the end
"""


class Solution:
    def alienOrder(self, words: List[str]) -> str:
        graphs = defaultdict(set)
        before = defaultdict(set)

        for i in range(len(words)):
            for j in range(i+1, len(words)):
                # edge case I missed and didn't think 
                if len(w1) > len(w2) and w1[:len(w2)] == w2:
                    return ""
                w1, w2 = words[i], words[j]
                for c1, c2 in zip(w1, w2):
                    if c1 != c2:
                        graphs[c1].add(c2)
                        graphs[c2].add(c1)
                        before[c2].add(c1)
                        break

        incomingLinks = [0]*26
        bfsQ = deque()
        for c in graphs:
            incomingLinks[ord(c)-ord('a')] = len(before[c])
            if incomingLinks[ord(c)-ord('a')] == 0:
                bfsQ.append(c)

        res = []
        while bfsQ:
            sz = len(bfsQ)
            while sz:
                c = bfsQ.popleft()
                res.append(c)

                for nextC in graphs[c]:
                    incomingLinks[ord(nextC)-ord('a')] -= 1
                    if incomingLinks[ord(nextC)-ord('a')] == 0:
                        bfsQ.append(nextC)
                sz -= 1

        # this is not edge case.. I should at least have this valid checking
        if len(res) != len(graphs):
            return ""

        for w in words:
            for c in w:
                if c not in graphs:
                    res.append(c)
                    graphs[c].add(c)

        return "".join(res)

"""
another edge case

Input: ["abc","ab"]
Output: "abc" 
Expected: ""

- I didn't verify if the topo sort is valid
- added this: this is an edge case to handle
                if len(w1) > len(w2) and w1[:len(w2)] == w2:
                    return ""
finally

Runtime: 39 ms, faster than 63.63% of Python3 online submissions for Alien Dictionary.
Memory Usage: 14 MB, less than 57.30% of Python3 online submissions for Alien Dictionary.

"""

if __name__ == '__main__':
    s = Solution()
    print(s.alienOrder(words=["abc", "ab"]))
    print(s.alienOrder(words=["wrt", "wrf", "er", "ett", "rftt"]))


        
