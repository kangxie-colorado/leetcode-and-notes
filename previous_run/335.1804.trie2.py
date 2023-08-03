"""
https://leetcode.com/problems/implement-trie-ii-prefix-tree/?envType=study-plan&id=programming-skills-iii

this adds a twist of counting the word
so think change the terminate flag to word count.. if it is not a word.. use a 0
"""


class Trie:

    def __init__(self):
        self.children = {}
        self.count = 0
        self.prefixCount = 0

    def insert(self, word: str) -> None:
        curr = self 

        for i,c in enumerate(word):
            if c not in curr.children:
                curr.children[c] = Trie()
            curr = curr.children[c]
            curr.prefixCount += 1
            if i==len(word)-1:
                curr.count += 1
        

    def countWordsEqualTo(self, word: str) -> int:
        curr = self

        for c in word:
            if c not in curr.children:
                return 0
            curr = curr.children[c]
        
        return curr.count


    def countWordsStartingWith(self, prefix: str) -> int:
        # to do this effcienlty
        # do I traverse down to each childen or maybe aggeragate the count upwards?
        curr = self

        for c in prefix:
            if c not in curr.children:
                return 0
            curr = curr.children[c]
        
        return curr.prefixCount


    def erase(self, word: str) -> None:
        curr = self
        for i, c in enumerate(word):
            curr = curr.children[c]
            curr.prefixCount -= 1
            if i == len(word)-1:
                curr.count -= 1
    
"""
Runtime: 409 ms, faster than 77.39% of Python3 online submissions for Implement Trie II (Prefix Tree).
Memory Usage: 28.7 MB, less than 33.04% of Python3 online submissions for Implement Trie II (Prefix Tree).
"""