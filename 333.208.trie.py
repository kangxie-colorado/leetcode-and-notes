"""
https://leetcode.com/problems/implement-trie-prefix-tree/

I thought I did this in python but no?

"""


class Trie:

    def __init__(self):
        self.children = {}
        self.terminate = False

    def insert(self, word: str) -> None:
        curr = self
        for i, c in enumerate(word):
            if c not in curr.children:
                curr.children[c] = Trie()
            curr = curr.children[c]
            if i == len(word)-1:
                curr.terminate =  True


    def search(self, word: str) -> bool:
        curr = self
        for c in word:
            if c not in curr.children:
                return False
            curr = curr.children[c]
        
        return curr.terminate

    def startsWith(self, prefix: str) -> bool:
        curr = self
        for c in prefix:
            if c not in curr.children:
                return False
            curr = curr.children[c]
        
        return True


"""
Runtime: 179 ms, faster than 88.06% of Python3 online submissions for Implement Trie (Prefix Tree).
Memory Usage: 31.5 MB, less than 73.44% of Python3 online submissions for Implement Trie (Prefix Tree).
"""