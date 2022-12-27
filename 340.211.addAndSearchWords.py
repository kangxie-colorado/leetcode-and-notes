"""
https://leetcode.com/problems/design-add-and-search-words-data-structure/

the dot is a pure headache
I thought I could build . into the trie but one word will turn into C_N_3*8 nodes..
so that is not wise at all..

then there really seems to be no optimization
maybe I can reverse the word.. and do that suffix search.. if it doesn't end with .

that could improve the time maybe a bit
anyway.. I meet it I solve it

no need to whine
"""


class TrieNode:
    def __init__(self) -> None:
        self.children = {}
        self.terminate = False


class WordDictionary:

    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:

        def addToTrie(word):
            curr = self.root
            for i, c in enumerate(word):
                if c not in curr.children:
                    curr.children[c] = TrieNode()
                curr = curr.children[c]
                if i == len(word)-1:
                    curr.terminate = True

        addToTrie(word)

    def search(self, word: str) -> bool:

        def searchInTrie(root, i, word):
            if i == len(word):
                return root.terminate
            c = word[i]
            if c == '.':
                for child in root.children.values():
                    if searchInTrie(child, i+1, word):
                        return True
            return c in root.children and searchInTrie(root.children[c], i+1, word)

        return searchInTrie(self.root, 0, word)


"""
Runtime: 7623 ms, faster than 70.59% of Python3 online submissions for Design Add and Search Words Data Structure.
Memory Usage: 78.1 MB, less than 47.33% of Python3 online submissions for Design Add and Search Words Data Structure.

Runtime: 7775 ms, faster than 69.92% of Python3 online submissions for Design Add and Search Words Data Structure.
Memory Usage: 78.2 MB, less than 24.30% of Python3 online submissions for Design Add and Search Words Data Structure.

now let me add the reverse logic into it
"""


class WordDictionary:

    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:

        def addToTrie(word, reversed=False):
            curr = self.root
            for i, c in enumerate(word):
                if c not in curr.children:
                    curr.children[c] = TrieNode()
                curr = curr.children[c]
                if i == len(word)-1:
                    curr.terminate = True
                    curr.reverse = reversed

        addToTrie(word)
        addToTrie(word[::-1], reversed=True)

    def search(self, word: str) -> bool:

        def searchInTrie(root, i, word, reversed=False):
            if i == len(word):
                return root.terminate and not (reversed and not root.reverse)
            c = word[i]
            if c != '.':
                return c in root.children and searchInTrie(root.children[c], i+1, word, reversed=reversed)
            else:
                for child in root.children.values():
                    if searchInTrie(child, i+1, word, reversed=reversed):
                        return True

            return False

        revWord = word[::-1]
        if '.' in word:
            idx = word.index('.')
            revIdx = revWord.index('.')
            if idx<revIdx:
                return searchInTrie(self.root, 0, revWord, reversed=True)
    
        return  searchInTrie(self.root, 0, word)

"""
okay. this didn't fly
don't over do..

"""

if __name__ == '__main__':
    wd = WordDictionary()
    wd.addWord('')
    wd.addWord('ab')
    print(wd.search('a'))