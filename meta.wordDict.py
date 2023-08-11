class TrieNode:
    def __init__(self):
        self.children = {}
        self.isWord = False
        

class WordDictionary:

    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        curr = self.root
        for idx,c in enumerate(word):
            if c not in curr.children:
                curr.children[c] = TrieNode()
            child = curr.children[c]
            if idx == len(word)-1:
                child.isWord = True
            curr= child

    def search(self, word: str) -> bool:
        def searchInTrie(root, idx):
            c = word[idx]
            if c == '.':
                if idx == len(word)-1:
                    return len(root.children) and any(child.isWord for chile in root.children.values())
                for child in root.children.values():
                    if searchInTrie(child, idx+1):
                        return True
                return False  
            else:
                if c not in root.children:
                    return False
                
                child = root.children[c]
                if idx == len(word) -1:
                    return child.isWord
                
                return searchInTrie(child, idx+1)
        
        return searchInTrie(self.root, 0)

    
if __name__ == '__main__':
    calls = ["WordDictionary","addWord","addWord","search","search","search","search","search","search"]
    params = [[],["a"],["a"],["."],["a"],["aa"],["a"],[".a"],["a."]]

    for call,param in zip(calls, params):
        if call == "WordDictionary":
            wd = WordDictionary(*param)
        elif call == 'addWord':
            wd.addWord(*param)
        else:
            print(wd.search(*param))