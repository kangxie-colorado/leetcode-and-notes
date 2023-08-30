from collections import deque
import heapq
from typing import List


class TrieNode:
    def __init__(self):
        self.children={}
        self.terminate = False
        self.count = 0 
         

class AutocompleteSystem:
    def insert(self, sentence, count):
        curr = self.root
        for i,c in enumerate(sentence):
            if c not in curr.children:
                curr.children[c] = TrieNode()
            
            child = curr.children[c]
            if i == len(sentence)-1:
                child.terminate = True
                child.count += count
            curr = child

    def __init__(self, sentences: List[str], times: List[int]):
        self.root = TrieNode()
        for sentence,count in zip(sentences,times):
            self.insert(sentence, count)
        
        self.runningSentence = []
        self.autocompleteNode = self.root

    def getTop3(self, node):
        baseSentence = "".join(self.runningSentence)
        q = deque([(node, baseSentence)])
        
        res = []
        while q:
            node, sentence = q.popleft()
            if node.terminate:
               res.append((node.count, sentence)) 
            for c in node.children:
                q.append((node.children[c], sentence+c))
        
        return [s for _,s in sorted(res, key=lambda x: (-x[0], x[1]))[:3]]
            
    def input(self, c: str) -> List[str]:
        if c=='#':
            self.insert(self.runningSentence,1)
            self.runningSentence = []
            self.autocompleteNode = self.root
            return
        
        self.runningSentence.append(c)
        curr = self.autocompleteNode
        if not curr or c not in curr.children:
            self.autocompleteNode = None
            return []
      
        curr = curr.children[c]
        res = self.getTop3(curr)
        self.autocompleteNode = curr

        return res


        



      
        
        
        


# Your AutocompleteSystem object will be instantiated and called as such:
# obj = AutocompleteSystem(sentences, times)
# param_1 = obj.input(c)