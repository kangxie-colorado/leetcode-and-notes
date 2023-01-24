"""
https://leetcode.com/problems/synonymous-sentences/

the data scope is not super big
0 <= synonyms.length <= 10
synonyms[i].length == 2
1 <= si.length, ti.length <= 10

so just group them together and do the multiply
"""


from collections import defaultdict
from typing import List


class Solution:
    def generateSentences(self, synonyms: List[List[str]], text: str) -> List[str]:

        roots = {w:w for p in synonyms for w in p} # let me try using map instead of array

        def find(w):
            if roots[w] != w:
                roots[w] = find(roots[w])
            return roots[w]
        
        def union(w1,w2):
            roots[find(w1)] = roots[find(w2)]
        
        for w1,w2 in synonyms:
            union(w1,w2)
        
        rootsToChiildren = defaultdict(list)
        for child in roots:
            root = find(child)
            rootsToChiildren[root].append(child)
        for root in rootsToChiildren:
            rootsToChiildren[root].sort()
        
        words = text.split()
        res = []
        def f(idx, run):
            if idx >= len(words):
                res.append(" ".join(run))
                return 
            
            if words[idx] not in roots:
                f(idx+1, run +[ words[idx]])
                return
            
            root = find(words[idx])
            for choice in rootsToChiildren[root]:
                f(idx+1, run + [choice])

        f(0,[])
        return res
    

"""
Runtime: 41 ms, faster than 46.04% of Python3 online submissions for Synonymous Sentences.
Memory Usage: 13.9 MB, less than 91.34% of Python3 online submissions for Synonymous Sentences.

let me see if I can simplify the code a bit
"""


class Solution:
    def generateSentences(self, synonyms: List[List[str]], text: str) -> List[str]:

        # let me try using map instead of array
        roots = {w: w for p in synonyms for w in p}

        def find(w):
            if roots[w] != w:
                roots[w] = find(roots[w])
            return roots[w]

        def union(w1, w2):
            r1, r2 = find(w1), find(w2)
            roots[r1] = roots[r2]

        for w1, w2 in synonyms:
            union(w1, w2)

        rootsToChildren = defaultdict(list)
        for child in roots:
            root = find(child)
            rootsToChildren[root].append(child)
        for root in rootsToChildren:
            rootsToChildren[root].sort()

        words = text.split()
        res = []

        def f(idx, run):
            if idx >= len(words):
                res.append(" ".join(run))
                return

            if words[idx] not in roots:
                f(idx+1, run + [words[idx]])
                return

            root = find(words[idx])
            for choice in rootsToChildren[root]:
                f(idx+1, run + [choice])

        f(0, [])
        return res

"""
I dont see a lot of simplification on top of my code 
this one's code is better and has many advanced features

https://leetcode.com/problems/synonymous-sentences/discuss/430489/python-union-find

        def find(x):
            uf.setdefault(x, x)     <-- I see it used somewhere/by-someone else
            if uf[x]!=x:
                uf[x] = find(uf[x])
            return uf[x]

        fin_res = [" ".join(sentence) for sentence in itertools.product(*res)]
        ^ this itertools.produc() is interesting
>>> a = [[1],[2],[3,4,5],[6,7],[9]]
>>> itertools.product(*a)
<itertools.product object at 0x10de25b80>
>>> list(itertools.product(*a))
[(1, 2, 3, 6, 9), (1, 2, 3, 7, 9), (1, 2, 4, 6, 9), (1, 2, 4, 7, 9), (1, 2, 5, 6, 9), (1, 2, 5, 7, 9)]
"""



if __name__ == '__main__':
    s = Solution()
    print(s.generateSentences(synonyms=[["happy", "joy"], ["sad", "sorrow"], [
          "joy", "cheerful"]], text="I am happy today but was sad yesterday"))
    print(s.generateSentences(synonyms=[["happy", "joy"], [
          "cheerful", "glad"]], text="I am happy today but was sad yesterday"))

