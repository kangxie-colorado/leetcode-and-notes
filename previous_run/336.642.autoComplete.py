"""
https://leetcode.com/problems/design-search-autocomplete-system/

okay.. this is a hard problem
and I have a starting point from trie11

the insert can be updated to take an initial count 
also how to get the top 3?
maybe just sort.. because there are at most 28 possibilities 

c is a lowercase English letter, a hash '#', or space ' '.
not that much.. no need to worry

well I'll settle for sort on spot
"""


from typing import List


class Trie:

    def __init__(self):
        self.children = {}
        self.count = 0

    def insert(self, word: str, count: int) -> None:
        curr = self

        for i, c in enumerate(word):
            if c not in curr.children:
                curr.children[c] = Trie()
            curr = curr.children[c]
            if i == len(word)-1:
                curr.count += count


class AutocompleteSystem:

    def __init__(self, sentences: List[str], times: List[int]):
        self.root = Trie()
        for sentence,time in zip(sentences, times):
            self.root.insert(sentence, time)
        
        self.search = ""


    def input(self, c: str) -> List[str]:
        if c == '#':
            self.root.insert(self.search, 1)
            self.search = ""
            return []

        def dfs(node, prefix):
            if not node:
                return []
            if not node.children:
                return [(-node.count, prefix)]
            
            coundAndPrefix = []
            if node.count:
                coundAndPrefix.extend([(-node.count, prefix)])
            for key, child in node.children.items():
                coundAndPrefix.extend(dfs(child, prefix+key))
            
            return coundAndPrefix

        res = []
        self.search += c
        curr = self.root
        for p in self.search:
            if p not in curr.children:
                curr = None
                break 
            curr = curr.children[p]
        
        countAndPrefix = dfs(curr, self.search)
        countAndPrefix.sort()

        res.extend([e[1]
                for e in countAndPrefix[:min(3, len(countAndPrefix))]])

        return res

"""
Runtime: 827 ms, faster than 71.03% of Python3 online submissions for Design Search Autocomplete System.
Memory Usage: 20.1 MB, less than 45.12% of Python3 online submissions for Design Search Autocomplete System.
"""

    
if __name__ == '__main__':
    s = AutocompleteSystem(
        ["i love you", "island", "iroman", "i love leetcode"], [5, 3, 2, 2])
    
    for c in "i a#":
        print(s.input(c))


