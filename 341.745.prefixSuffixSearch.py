"""
https://leetcode.com/problems/prefix-and-suffix-search/

just try a bit
dont push too hard

thinkings
1. build a prefix trie (at the end, save the max index of that word)
2. build a suffix trie

on search
1. search the suffix.. if not here, return 
2. then search the prefix.. if not here, return
if both exist.. search suffix from the prefix node

I don't know better just I think I can try a bit 


"""


from collections import defaultdict
from typing import List
# from functools import cache




class TrieNode:
    def __init__(self) -> None:
        self.children = {}
        self.words = set()


class WordFilter:
    def __init__(self, words: List[str]):
        self.index = 0
        self.prefixTrie = TrieNode()
        self.suffixTrie = TrieNode()

        for word in words:
            self.addToTrie(self.prefixTrie, word)
            self.addToTrie(self.suffixTrie, word[::-1])
            self.index += 1

    def addToTrie(self, root, word):
        curr = root
        for c in word[:min(len(word), 7)]:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
            curr.words.add(self.index)

    def words(self, root, prefix):
        curr = root
        for p in prefix:
            if p not in curr.children:
                return None
            curr = curr.children[p]

        return curr.words

    # @cache
    def f(self, pref: str, suff: str) -> int:
        suffixSet = self.words(self.suffixTrie, suff[::-1])
        prefixSet = self.words(self.prefixTrie, pref)

        if suffixSet and prefixSet:
            interSet = suffixSet.intersection(prefixSet)
            if interSet:
                return max(interSet)

        return -1


"""
7 / 17 test cases passed.


it is TLE>. 
looks like I can use a cache

Runtime: 4272 ms, faster than 46.21% of Python3 online submissions for Prefix and Suffix Search.
Memory Usage: 202.8 MB, less than 13.78% of Python3 online submissions for Prefix and Suffix Search.

hahahahah...
check out other solutions tomorrow

and I don't feel like trie is important at all here
just use hashmaps.. may do it as well
"""


class WordFilter:

    def __init__(self, words: List[str]):
        self.prefixMap = defaultdict(set)
        self.suffixMap = defaultdict(set)
        for idx, word in enumerate(words):
            for i in range(min(7, len(word))):
                self.prefixMap[word[:i+1]].add(idx)
                self.suffixMap[word[-1:]].add(idx)

    def f(self, pref: str, suff: str) -> int:
        interSet = self.prefixMap[pref].intersection(self.suffixMap[suff])
        if len(interSet):
            return max(interSet)
        return -1

"""
also TLE

use cache and 
Runtime: 1650 ms, faster than 92.97% of Python3 online submissions for Prefix and Suffix Search.
Memory Usage: 159.6 MB, less than 23.51% of Python3 online submissions for Prefix and Suffix Search.


and the tips are golden

Take "apple" as an example, we will insert add "apple{apple", "pple{apple", "ple{apple", "le{apple", "e{apple", "{apple" into the Trie Tree.
If the query is: prefix = "app", suffix = "le", we can find it by querying our trie for "le { app".
We use '{' because in ASCii Table, '{' is next to 'z', so we just need to create new TrieNode[27] instead of 26. Also, compared with traditional Trie, we add the attribute weight in class TrieNode. You can still choose any different character.
"""


class TrieNode:
    def __init__(self) -> None:
        self.children = {}
        self.index = -1


class WordFilter:

    def __init__(self, words: List[str]):
        self.root = TrieNode()
        

        for idx, word in enumerate(words):         
            wordPrefixWrap = word[:min(7, len(word))]
            for i in range(1, min(7, len(word))+1):
                insertWord = word[-i:] + '{' + wordPrefixWrap
                curr = self.root
                for c in insertWord:
                    if c not in curr.children:
                        curr.children[c] = TrieNode()
                    curr = curr.children[c]
                    curr.index = idx

    
    def f(self, pref: str, suff: str) -> int:
        searchTerm = suff+'{'+pref

        curr = self.root
        for c in searchTerm:
            if c not in curr.children:
                return -1
            
            curr = curr.children[c]
        return curr.index

"""
Runtime: 4860 ms, faster than 37.29% of Python3 online submissions for Prefix and Suffix Search.
Memory Usage: 203.5 MB, less than 13.51% of Python3 online submissions for Prefix and Suffix Search.
"""

if __name__ == '__main__':
    wf = WordFilter(['abba'])
    print(wf.f('ab', 'ba'))