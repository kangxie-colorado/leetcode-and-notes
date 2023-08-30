
from typing import List


class TrieNode:
    def __init__(self):
        self.children = {}
        self.terminate = False

class StreamChecker:
    def insertWord(self, word):
        curr = self.root 

        for i,c in enumerate(word):
            if c not in curr.children:
                curr.children[c] = TrieNode()
        
            curr = curr.children[c]
            if i == len(word)-1:
                curr.terminate = True            

    def __init__(self, words: List[str]):
        self.root = TrieNode()
        self.curr = self.root 
        for word in words:
            self.insertWord(word)        

    def query(self, letter: str) -> bool:
        if letter in self.curr.children:
            self.curr = self.curr.children[letter]
            if self.curr.terminate:
                return True
        else:
            if self.curr != self.root:
                self.curr = self.root
                return self.query(letter)

        return False
        
""""
of course not correct
thinking if I can reverse insert
"""

class StreamChecker:
    def reverseInsertWord(self, word):
        curr = self.root 
        i = len(word)-1
        while i>=0:
            c = word[i]
            if c not in curr.children:
                curr.children[c] = TrieNode()
        
            curr = curr.children[c]
            if i == 0:
                curr.terminate = True            

    def __init__(self, words: List[str]):
        self.root = TrieNode()
        self.letters = []
        for word in words:
            self.reverseInsertWord(word)        

    def query(self, letter: str) -> bool:
        self.letters.append(letter)
        curr = self.root
        idx = len(self.letters)-1
        while idx>=0:
            c = self.letters[idx]
            if c not in curr.children:
                break
            curr = curr.children[c]
            if curr.terminate:
                return True
            idx -= 1

        return False