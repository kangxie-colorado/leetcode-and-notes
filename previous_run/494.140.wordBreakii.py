"""
https://leetcode.com/problems/word-break-ii/?envType=study-plan&id=dynamic-programming-iii

so straight forward
if s[:i+1] is a word.. you can either break or not.. 


"""


from collections import defaultdict
from typing import List


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        res = []
        n = len(s)
        wordSet = set(wordDict)
        def f(idx, run):
            if idx==len(s):
                res.append(" ".join(run))
                return
            
            for nextBreak in range(idx+1, n+1):
                if s[idx:nextBreak] in wordSet:
                    f(nextBreak, run+[s[idx:nextBreak]])
        f(0,[])
        return res

"""
Runtime: 30 ms, faster than 79.21% of Python3 online submissions for Word Break II.
Memory Usage: 13.8 MB, less than 74.14% of Python3 online submissions for Word Break II.

Runtime: 29 ms, faster than 82.14% of Python3 online submissions for Word Break II.
Memory Usage: 13.9 MB, less than 25.74% of Python3 online submissions for Word Break II.

this problem probably has a lot of solutions
let me see the dp one
"""


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        res = []
        n = len(s)
        wordSet = set(wordDict)

        def f(idx):
            if idx == len(s):
                return [""]

            res = []
            for nextBreak in range(idx+1, n+1):
                word = s[idx:nextBreak]
                if word in wordSet:
                    for subRes in f(nextBreak):
                        res.append((word+" "+subRes).strip())
                    
            return res
        return f(0)

"""
Runtime: 30 ms, faster than 79.21% of Python3 online submissions for Word Break II.
Memory Usage: 14 MB, less than 25.74% of Python3 online submissions for Word Break II.

interesting.. using cache it is worse..

okay there is a trie based solution 
that can help compress the space.. and maybe some time

leave that to future practice
"""

class TrieNode:
    def __init__(self) -> None:
        self.children = defaultdict(set)
        self.terminal = False 

    def addWord(self, word):
        curr = self 
        for i,c in enumerate(word):
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
            if i == len(word)-1:
                curr.terminal = True


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        trieRoot = TrieNode()

        for word in wordDict:
            trieRoot.addWord(word)

        res = []

        def f(i, run):
            if i == len(s):
                res.append(" ".join(run))
                return

            curr = trieRoot
            for j in range(i, len(s)):
                if s[j] in curr.children:
                    curr = curr.children[s[j]]
                    if curr.terminal:
                        f(j+1, run + [s[i:j+1]])
                else:
                    break
        f(0, [])
        return res


# adding pruning with memorization
# so this shows me a way to memorization on something other that the major results
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        trieRoot = TrieNode()

        for word in wordDict:
            trieRoot.addWord(word)
        
        res = []
        canNotBreak = set()
        def breakWord(i, run):
            if i == len(s):
                res.append(" ".join(run))
                return True
            
            if i in canNotBreak:
                return False
            
            curr = trieRoot
            success = False
            for j in range(i, len(s)):
                if s[j] in curr.children:
                    curr = curr.children[s[j]]
                    if curr.terminal:
                        if breakWord(j+1, run + [s[i:j+1]]):
                            success |= True
                else:
                    break  
            if not success:
                canNotBreak.add(i)
            
            return success
            
        breakWord(0,[])
        return  res

"""
Runtime: 38 ms, faster than 27.95% of Python3 online submissions for Word Break II.
Memory Usage: 13.8 MB, less than 74.07% of Python3 online submissions for Word Break II.

okay... now adding memorization for pruning the false cases

Runtime: 27 ms, faster than 89.61% of Python3 online submissions for Word Break II.
Memory Usage: 13.9 MB, less than 26.01% of Python3 online submissions for Word Break II.


okayt.. good enough
"""


if __name__ == '__main__':
    s = Solution()
    print(s.wordBreak(s="catsanddog", wordDict=[
          "cat", "cats", "and", "sand", "dog"]))
