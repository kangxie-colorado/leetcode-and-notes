"""
https://leetcode.com/problems/design-file-system/?envType=study-plan&id=programming-skills-iii

"""
class TrieNode:
    def __init__(self) -> None:
        self.children = {}
        self.value = -1


class FileSystem:

    def __init__(self):
        self.root = TrieNode()


    def createPath(self, path: str, value: int) -> bool:
        dirs = path.split('/')[1:]

        curr = self.root 
        for i, dir in enumerate(dirs):
            if dir not in curr.children:
                if i != len(dirs)-1:
                    return False
                else:
                    curr.children[dir] = TrieNode()
            curr = curr.children[dir]
            if i == len(dirs)-1:
                if curr.value != -1:
                    return False
                curr.value = value
        
        return True
        

    def get(self, path: str) -> int:
        dirs = path.split('/')[1:]

        curr = self.root 
        for i, dir in enumerate(dirs):
            if dir not in curr.children:
                return -1
                
            curr = curr.children[dir]
            if i == len(dirs)-1:
                return curr.value
            
        return -1

"""
Runtime: 296 ms, faster than 85.29% of Python3 online submissions for Design File System.
Memory Usage: 21.8 MB, less than 46.77% of Python3 online submissions for Design File System.
"""